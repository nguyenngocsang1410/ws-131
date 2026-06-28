# 08 — Security Posture

Assessment from a multi-agent audit whose findings were each **adversarially re-verified
against the live host** (2026-06-28). Bottom line: **the application/identity design is sound;
the weakness is at the network/host layer.**

## Strengths (verified)

- **TLS** at nginx is modern: TLSv1.2/1.3 only, prefer-server-ciphers, session tickets off,
  2048-bit `ffdhe2048` DH param (adequate). Private key is 0600 root.
- **Secrets** are wallet-isolated: `secrets.json` is a *manifest* (no raw values); key material
  in `etc/wallets/` is 0700; the DB password resolves from a wallet at runtime, not from config.
- **Data stores** PostgreSQL, Redis, Solr all bind `127.0.0.1` only.
- **MFA** — a TOTP 2FA authenticator (`cs.mfa`) is installed and active.
- **Auth** is a self-hosted OIDC stack (oidc_server / ologin / gatekeeper) with `ElementsAuth`.

## Findings

| # | Sev | Finding | Evidence |
|---|---|---|---|
| 1 | **High** | **No inbound host firewall** — `ufw` inactive, iptables/nft `INPUT` policy `ACCEPT` (only Tailscale chains). All `0.0.0.0` ports are network-reachable. | `ufw status`=inactive; `iptables -S INPUT` → `-P INPUT ACCEPT` |
| 2 | **High** | **Backends bypass nginx** — `cdbsrv :8080`, blobstore :8082, ologin :8083, oidc :8084, gatekeeper :8085, broker :8086, HOOPS :8087, role_cache :8888 all bind `0.0.0.0` and answer plain HTTP directly (probed 8080→307, 8082→302, 8085→400). nginx proxies only to `127.0.0.1`. | `ss -tlnp`; curl probes |
| 3 | **Med** | **Unauthenticated Apache Tika 3.3.1 on `0.0.0.0:9998`** (`auth: null`). SSRF/XXE/RCE-prone; can pivot to the loopback-only stores. | `ps --host 0.0.0.0`; `curl :9998/version` |
| 4 | **Med** | **Redis has no password** (`requirepass` empty); backs sessions/OIDC state. Loopback-only → local risk (read/forge sessions & tokens). | `redis-cli config get requirepass` |
| 5 | **Med** | **World-readable config** under `instance/etc` (0664), incl. `secrets.json`, `oidc_auth.json`, `dbtab.yml`. Config disclosure (mitigated: real keys 0700). | `ls -l instance/etc` |
| 6 | **Med** | **Plaintext DB password in the install PDFs** (`raw/contact/install-docs/`). Live host mitigates via wallet indirection, but the notes leak a live credential. | the 4 PDFs (value not reproduced) |
| 7 | **Med** | **3D broker not proxied** — advertised at `https://plm_vsi/broker` but nginx has no `/broker` location; reached via the exposed `0.0.0.0:8086`/`:8087`. | `services.json`; `nginx.conf` |
| 8 | **Low** | **Self-signed internal TLS cert** (CN=`plm_vsi`, issuer SoluCA, no CA chain). | `openssl x509` |
| 9 | **Low** | **Auto-unlock wallets** — unlock material on-disk → host compromise yields service creds. | `secrets.json` `default_auto_unlock` |
| 10 | **Low** | **Co-tenant exposure** — unrelated Docker container on `0.0.0.0:8010` (bypasses host-firewall intent). | `docker ps`; nft DOCKER DNAT |
| 11 | **Low** | **Oracle client libs bundled** in `cdbwrapc` (23.1) despite Postgres backend — dormant surface. | `cdbwrapc/*.so` |
| 12 | **Low** | **Stale module trains** — CAD/Office/Workspaces 15.x; ecm/licdash/licreport/msteams 16.1.x. | dist-info versions |

> **Existing firewall caveat:** the host *does* run an nftables `vsi_lockdown` table, but it is
> an **egress, uid-scoped** block (stops user `vsi` reaching the public internet). It has an
> `output` chain only — it does **not** filter inbound traffic, so it does not mitigate findings
> #1–#2. (See `wiki/concepts/internet-lockdown-vsi.md`.) Also note `vsi` is in `sudo`, so even
> the egress block is bypassable via `sudo`.

## Remediation checklist (priority order)

- [ ] **Enable an inbound host firewall** — allow only `80/443` (+ ssh from trusted nets); drop
      the rest. *Or* rebind every CONTACT backend to `127.0.0.1` (it's all behind nginx anyway).
- [ ] **Bind Tika to `127.0.0.1:9998`** (only used over loopback) — change `tika.service`
      `--host 0.0.0.0` → `--host 127.0.0.1`.
- [ ] **Set a Redis password** (`requirepass`) and update the `services.json` wallet.
- [ ] **Tighten `instance/etc` permissions** — remove world-read, especially on `secrets.json`.
- [ ] **Scrub/secure the plaintext DB password** in the install notes; rotate if those notes
      circulated.
- [ ] **Add an nginx `/broker` location** (or firewall `:8086`/`:8087`).
- [ ] **Replace the self-signed cert** with a properly-issued one (with SAN) if feasible.
- [ ] **Patch-currency review** of the 15.x/16.1.x modules + the bundled Tika/Oracle libs.
- [ ] **Confirm 2FA enforcement** (see open questions).

## Open questions

- Is TOTP 2FA *enforced* for all logins or opt-in? (`oidc_auth.json` default ACR is
  password-"sufficient" while `cs.mfa` TOTP is active — the enforcement chain is unclear.)
- Are the `0.0.0.0` ports shielded by an upstream network firewall/segmentation off-host?
- Where does the wallet auto-unlock key live, and what are its perms?
- Does blobstore (`:8082`) enforce auth for direct/presigned blob access?

→ Next: [09-installation.md](09-installation.md)

---
title: CONTACT PLM security posture
type: concept
created: 2026-06-28
updated: 2026-06-28
sources: [session:claude-code/2026-06-28]
tags: [contact-software, plm, security, exposure, firewall, tika, oidc, secrets]
status: stable
---

# CONTACT PLM security posture

Assessment of the [[opt-contact]] deployment's security, from a multi-agent audit whose
findings were each adversarially re-verified against the live host (2026-06-28).

## Summary
**The application/identity design is sound; the weakness is at the network/host layer.**
Auth is a self-hosted OIDC stack with a modern TLS front ([[contact-plm-architecture]]),
TOTP 2FA is installed and active, secrets are wallet-isolated (not plaintext), and all data
stores except Tika are loopback-only. But there is **no host firewall**, and **every CONTACT
backend binds `0.0.0.0`**, so the nginx TLS/auth front door can be bypassed on the LAN — and
an **unauthenticated Apache Tika** sits on `0.0.0.0:9998`. Several lower issues (world-readable
config, passwordless Redis, self-signed cert, a plaintext DB password in the install PDFs)
compound local/lateral risk.

## Confirmed issues (verified against the live system)

| Sev | Issue | Evidence |
|---|---|---|
| **High** | **No host firewall** — `ufw` inactive, iptables/nft `INPUT` policy `ACCEPT` (only Tailscale chains). All `0.0.0.0` ports are network-reachable. | `ufw status`=inactive; `iptables -S INPUT` → `-P INPUT ACCEPT` |
| **High** | **Backends bypass the nginx front door** — `cdbsrv :8080`, blobstore :8082, ologin :8083, oidc :8084, gatekeeper :8085, broker :8086, HOOPS :8087, role_cache :8888 all bind `0.0.0.0` and answer plain HTTP directly (probed: 8080→307, 8082→302, 8085→400, 8086→403). nginx only proxies to `127.0.0.1`. | `ss -tlnp`; curl probes |
| **Med** | **Unauthenticated Apache Tika 3.3.1 on `0.0.0.0:9998`** — `auth: null`; serves `/version` etc. unauthenticated. Tika has a long SSRF/XXE/RCE history and can pivot to the loopback-only stores. | `ps` `--host 0.0.0.0`; `curl :9998/version`→`Apache Tika 3.3.1`; `services.json` cdb.tika auth null |
| **Med** | **Redis has no password** (`requirepass` empty) — backs sessions, ologin & OIDC state. Loopback-only, so the risk is local: any local process can read/forge sessions/tokens. | `redis-cli config get requirepass`→empty; `services.json` |
| **Med** | **World-readable config** under `instance/etc` (mode 0664), incl. `secrets.json`, `oidc_auth.json`, `dbtab.yml`. Any local user can map the secret/wallet topology, DB layout, OIDC config. (**Mitigated:** `secrets.json` holds only wallet *metadata*; real keys in `wallets/` are 0700.) | `ls -l instance/etc` |
| **Med** | **Plaintext DB password in the install PDFs** (`CREATE USER … WITH PASSWORD '…'`) in `raw/contact/install-docs/`. Live host mitigates via `$(CADDOK_DB_PASSWORD)` wallet indirection, but the notes leak a live credential. (Value deliberately not recorded here; PDFs even disagree on spelling — a typo.) | the 4 PDFs; cf. `dbtab.yml` |
| **Med** | **3D broker route declared but not proxied** — `services.json` advertises `https://plm_vsi/broker` but nginx has no `/broker` location; 3D is reached via the directly-exposed `0.0.0.0:8086`/`:8087`. | `services.json`; `nginx.conf` |
| **Low** | **Self-signed internal TLS cert** (CN=`plm_vsi`, issuer=SoluCA, no CA chain). Key is 0600 root; TLS itself is modern (TLSv1.2/1.3, 2048-bit ffdhe2048 DH param — **adequate**, the small `dhparam.pem` is just a 2048-bit param). | `openssl x509`; `nginx.conf` |
| **Low** | **Auto-unlock wallets** — all `secrets.json` entries `default_auto_unlock`; unlock material is on-disk, so host compromise yields service creds. | `secrets.json`; `wallets/` 0700 |
| **Low** | **Co-tenant exposure** — an unrelated Docker container publishes `0.0.0.0:8010` (filter-v2-api), bypassing host-firewall intent; out of CONTACT's patch lifecycle. | `docker ps`; nft DOCKER DNAT |
| **Low** | **Oracle client libs bundled** in `cdbwrapc` (libclntsh 23.1) though backend is PostgreSQL — dormant attack surface. | `cdbwrapc/` .so files |
| **Low** | **Stale module trains** — CAD/Office/Workspaces on 15.x, a few modules 16.1.x, vs 16.2 core ([[contact-plm-modules]]). | dist-info versions |

> **Note on the existing nftables lockdown:** the host *does* run an nftables firewall — but
> [[internet-lockdown-vsi]] is an **egress**, uid-scoped block (stops user `vsi` reaching the
> public internet). It has an `output` chain only and does **not** filter inbound traffic, so
> it does not mitigate the `0.0.0.0` inbound exposure above. The `INPUT`/ingress policy is
> still `ACCEPT`. (No contradiction between "no inbound firewall" here and that egress lockdown.)

## What is *not* a problem (refuted or mitigated)
- **DH params**: 2048-bit ffdhe2048 — fine (an earlier "424-byte file looks weak" worry was wrong).
- **Secrets at rest**: `secrets.json` is a wallet *manifest*, not raw secrets; key material in `wallets/` is 0700; DB/service creds resolve from wallets at runtime, not from config.
- **Data stores**: PostgreSQL, Redis, Solr all bind `127.0.0.1` only (Tika is the lone exception).
- **MFA**: a TOTP 2FA authenticator (`cs.mfa`) is active (`active=1`).

## Top remediations (in order)
1. Enable a host firewall (allow only 80/443 + ssh from trusted nets); or rebind every CONTACT backend to `127.0.0.1`.
2. Bind Tika to `127.0.0.1:9998` (it's only used over loopback).
3. Set a Redis `requirepass`.
4. Tighten `instance/etc` perms (drop world-read, esp. `secrets.json`); purge/secure the plaintext password in the install notes.
5. Patch-currency review of the 15.x/16.1.x modules.

## Open questions
- Is TOTP 2FA *enforced* for all logins, or opt-in? (`oidc_auth.json` default ACR is password-"sufficient" while `cs.mfa` TOTP is active — enforcement chain unclear.)
- Are the `0.0.0.0` ports shielded by an upstream network firewall/segmentation off-host (only Tailscale ACLs exist on-host)?
- Where does the wallet auto-unlock key live, and what are its perms?
- Does blobstore (`:8082`) enforce auth for direct/presigned blob access?

## Related
- [[contact-plm-architecture]] — the nginx front door & trust boundary
- [[contact-plm-data-tier]] — Tika/Redis/Solr exposure
- [[contact-plm-config]] — wallet-based secrets, world-readable etc
- [[contact-offline-install]] — where the plaintext DB password originates
- [[internet-lockdown-vsi]] — the existing (egress-only) nftables firewall on this host
- [[opt-contact]] · [[vsi-precision-3680]]

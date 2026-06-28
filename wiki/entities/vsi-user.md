---
title: vsi (the user account)
type: entity
created: 2026-06-28
updated: 2026-06-28
sources: [session:claude-code/2026-06-28]
tags: [user, account, linux, security]
status: stable
---

# vsi (user account)

The primary local login account on [[vsi-precision-3680]] — distinct from the machine,
which shares the `vsi-` name.

## Summary
`vsi` is uid 1000, gid 1000 (home `/home/vsi`, shell `/bin/bash`), the lowest-numbered and
likely original account on the box. As of 2026-06-28 it is the subject of
[[internet-lockdown-vsi]]: blocked from the public internet.

## Details
- Groups: `vsi adm cdrom sudo dip plugdev users lpadmin` — **member of `sudo`**.
- Other real users on the host: `vietnq37` (uid 1001, the operator / control user),
  `duongpt29`, `dattt48`, `sangnn10`, `huyntg`, `haibt15`.
- Security note: because vsi can `sudo`, the UID-owner internet block can be bypassed by
  running commands as another uid — see the caveat in [[internet-lockdown-vsi]] and
  [[nftables-uid-owner-block]].

## Related
- [[internet-lockdown-vsi]] — current restriction on this account
- [[vsi-precision-3680]] — the host it lives on
- [[nftables-uid-owner-block]] — how the block targets this uid

## Open questions
- Should vsi be removed from `sudo` to make the lockdown bypass-proof?

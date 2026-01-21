# ♻️ android homelab node: The Pocket HomeLab

> **Turning "E-Waste" into a High-Performance Privacy & Cloud Node.**

## Overview

This project documents the conversion of a retired **OnePlus 5 (Snapdragon 835)** into a dedicated, always-on Linux server. By leveraging **Termux** and a rooted Android environment, this device now serves as the primary network gateway for all my mobile traffic.

It functions as a **global ad-blocker**, **VPN exit node**, and **private cloud storage**, effectively replacing paid services like Google One and commercial VPNs.

## Key Achievements

- **368 Mbps Mobile Speed:** Bypassed ISP throttling on public networks by tunneling traffic through home fiber via Tailscale.
- **96% Ad-Blocking Rate:** Network-wide DNS filtering via AdGuard Home.
- **IPv6 Leak Patch:** Custom routing to prevent Android IPv6 leaks, ensuring 100% DNS compliance.
- **40GB Private Cloud:** Self-hosted `File Browser` accessible from anywhere in the world.
- **Zero Cost:** Built entirely on existing hardware and open-source software.

## The Stack

| Component          | Technology      | Purpose                                         |
| :----------------- | :-------------- | :---------------------------------------------- |
| **OS Environment** | Termux (Rooted) | The Linux subsystem running on Android.         |
| **Networking**     | Tailscale       | Mesh VPN & Exit Node to route traffic securely. |
| **DNS Filtering**  | AdGuard Home    | Network-wide ad & tracker blocking.             |
| **Storage**        | File Browser    | Web-based file manager (Private Google Drive).  |
| **Remote Access**  | OpenSSH         | Managing the server via CLI.                    |

## Architecture

```mermaid
graph TD;
    Client[Nothing Phone 2a] -->|Tailscale Tunnel| Server[OnePlus 5 Node];
    Server -->|DNS Query| AdGuard[AdGuard Home];
    AdGuard --|Block| Ads[Advertisers / Trackers];
    AdGuard --|Allow| Internet[The Internet];
    Server -->|Storage Access| Cloud[File Browser /sdcard];
```

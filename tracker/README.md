# Nilanjan's Tracker

View https://nilansa.github.io/tracker/ — plain HTML, CSS and vanilla JavaScript.

- Today, upcoming, conferences, projects and research, meetings, all tasks, and completed/removed archive.
- Add/edit tasks, due dates and times in IST, source links, notes, in-progress/done/removed status and optional pin to Today.
- Local edits are saved automatically in this browser using localStorage, even when offline. Export/import JSON lets you back up tasks.
- The public website does not include real private tasks or emails. Initial rows are marked examples.
- An optional Private sync and backup section connects to private repository nilansa/nilanjan-tracker-data, path tasks.json. A fine-grained GitHub token restricted to that repository, with Contents read/write, is entered on your own device, never pasted into the assistant, and never committed to this repository. By default token is stored in browser sessionStorage; remember-on-device opt-in is less secure. All Pages scripts on nilansa.github.io share the same browser origin, so only use this option on a trusted device/site.
- Browser sync pulls and pushes via GitHub REST API, with merge by stable task id and updatedAt, preserving removed records. It polls while connected. The assistant can read changes on the same private JSON through the authorized GitHub connector. Avoid concurrent rapid edits on several devices.
- The three-hour assistant email/calendar scan, when scheduled, writes to the private repository, not this public one. GitHub Pages itself cannot perform unattended email scans or private writes: the assistant automation and private repo are separate components.
- If not connected, ChatGPT cannot see edits saved only in browser localStorage. Sync first or use JSON export to share those changes.

No JavaScript libraries, analytics, trackers, or remote assets.

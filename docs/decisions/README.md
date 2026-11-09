# Decision records

One file per decision: `DNNN-short-name.md`. Never delete or rewrite a decided record; a new record supersedes it (`supersedes: D00X`) and the old one gets `status: superseded`.

Front matter fields (the state generator reads them):

| Field | Values |
| --- | --- |
| `id` | `D001`, `D002`, … |
| `title` | Short name |
| `status` | `accepted` · `proposed` (waiting for approval) · `open` (not decided) · `superseded` |
| `date` | Date decided or last changed (YYYY-MM-DD) |
| `decided_by` | Who approved it (supervisor, team, university) |
| `owner` | Who drives an open or proposed decision to closure |
| `changes_proposal` | `true` if it changes the official proposal; name the section in the body |
| `follow_up` | List of open sub-questions or actions |

A Claude session may create a record only with `status: proposed` or `open`. Only people change a record to `accepted`.

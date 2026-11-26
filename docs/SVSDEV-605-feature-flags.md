# SVSDEV-605: feature flags for the Schutzwerk audit instance

The audit instance is configured in its own Ansible inventory group. Its explicit feature flags restore the DBC settings recorded immediately before SVSDEV-370, with OAuth login disabled as requested. This is a configuration comparison, not a claim that every product capability is enabled.

“Not set” means the key was absent from DBC's pre-SVSDEV-370 Ansible configuration and the application default applies. The SVSDEV-370 column shows its resulting DBC configuration after that change. Values for the audit instance reflect the new `ansible/group_vars/audit/instance_cfg.yml` and `with.yml`.

| Flag / setting | In plain language | DBC before SVSDEV-370 | DBC after SVSDEV-370 | Schutzwerk audit instance |
| --- | --- | --- | --- | --- |
| `FEATURE_NOTIFICATIONS_ENABLED` | Shows and processes in-app notifications. | `true` | `true` | `true` |
| `FEATURE_MINT_PAGES_ENABLED` | Enables the MINT learning pages. | `true` | `true` | `true` |
| `FEATURE_MULTIPLE_S3_PROVIDERS_ENABLED` | Allows files to use more than one S3 storage provider. | `true` | `true` | `true` |
| `FEATURE_VIDEOCONFERENCE_ENABLED` | Enables video conferences in courses and rooms. | Not set (application default) | `false` | Not set (application default) |
| `FEATURE_VIDEOCONFERENCE_WAITING_ROOM_ENABLED` | Enables the waiting room before a video conference. | `true` | `false` | `true` |
| `FEATURE_USER_MIGRATION_ENABLED` | Enables the administrator's user migration tools. | `true` | `false` | `true` |
| `FEATURE_ALERTS_ON_HOMEPAGE_ENABLED` | Shows alerts on the home page. | `false` | `false` | `false` |
| `FEATURE_COMMON_CARTRIDGE_COURSE_EXPORT_ENABLED` | Exports courses in Common Cartridge format. | `true` | `true` | `true` |
| `FEATURE_COMMON_CARTRIDGE_COURSE_IMPORT_ENABLED` | Imports courses in Common Cartridge format. | `true` | `false` | `true` |
| `FEATURE_TEAM_CREATE_ROOM_ENABLED` | Lets users create rooms from a team. | `true` | `false` | `true` |
| `FEATURE_COLUMN_BOARD_EXTERNAL_TOOLS_ENABLED` | Allows external tools to be added to column boards. | Not set (application default) | `true` | Not set (application default) |
| `FEATURE_MEDIA_SHELF_ENABLED` | Enables media shelf content in column boards. | Not set (application default) | `true` | Not set (application default) |
| `FEATURE_COURSE_SHARE` | Allows courses to be shared. | Not set (application default) | `false` | Not set (application default) |
| `FEATURE_LESSON_SHARE` | Allows lessons to be shared. | Not set (application default) | `false` | Not set (application default) |
| `FEATURE_TASK_SHARE` | Allows tasks to be shared. | Not set (application default) | `false` | Not set (application default) |
| `FEATURE_SCHOOL_DATA_READONLY_ENABLED` | Makes school data read-only in the relevant administration flows. | Not set (application default) | `true` | Not set (application default) |
| `FEATURE_TEAMS_INVITE_EXTERNAL_ENABLED` | Allows people outside a team to be invited to it. | Not set (application default) | `false` | Not set (application default) |
| `FEATURE_SCHULCONNEX_COURSE_SYNC_ENABLED` | Synchronizes courses through Schulconnex. | Not set (application default) | `false` | Not set (application default) |
| `FEATURE_ROOM_COPY_ENABLED` | Allows rooms to be copied. | Not set (application default) | `false` | Not set (application default) |
| `FEATURE_ROOM_SHARE` | Allows rooms to be shared. | Not set (application default) | `false` | Not set (application default) |
| `FEATURE_ROOM_ADD_EXTERNAL_PERSONS_ENABLED` | Allows external people to be added to rooms. | Not set (application default) | `false` | Not set (application default) |
| `FEATURE_ROOM_REGISTER_EXTERNAL_PERSONS_ENABLED` | Allows external people to register for rooms. | Not set (application default) | `false` | Not set (application default) |
| `FEATURE_ROOM_LINK_INVITATION_EXTERNAL_PERSONS_ENABLED` | Allows external people to join rooms through an invitation link. | Not set (application default) | `false` | Not set (application default) |
| `FEATURE_EXTERNAL_PERSON_REGISTRATION_ENABLED` | Enables the external-person registration flow. | Not set (application default) | `false` | Not set (application default) |
| `FEATURE_OAUTH_LOGIN_ENABLED` | Offers OAuth-based single sign-on. | Not set in DBC's group config | Instance-specific | `false` (disabled) |
| `WITH_LDAP` | Includes LDAP integration and sync services. | `true` | `false` in DBC group config | `true` |
| `WITH_COMMON_CARTRIDGE` | Includes Common Cartridge import/export support. | `true` | `true` | `true` |
| `WITH_NOTIFICATION_SERVER` | Includes the notification server service. | `true` | `false` | `true` |

The audit instance intentionally does not inherit the post-SVSDEV-370 DBC group settings. For flags absent before SVSDEV-370, this preserves application defaults rather than copying the explicit values added for DBC in that change.

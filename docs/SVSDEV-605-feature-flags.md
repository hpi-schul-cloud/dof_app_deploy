# SVSDEV-605: feature configuration for the Schutzwerk audit instance

The audit instance uses BRB's effective feature configuration while remaining in its own Ansible group. The comparison below shows DBC's effective settings immediately before SVSDEV-370, DBC's settings after that change, and the BRB settings. FWU is the exception: it remains disabled in audit until its required instance preparation is done.

The pre-SVSDEV-370 column uses the parent revision of the SVSDEV-370 commit plus shared Ansible defaults. “Not configured” means no value was specified for that flag in the relevant inventory or shared configuration. The BRB column reflects `group_vars/brb/instance_cfg.yml`, `group_vars/brb/with.yml`, and shared defaults. The audit group only overrides values where it must differ from those shared defaults.

| Flag / setting | In plain language | DBC before SVSDEV-370 | DBC after SVSDEV-370 | BRB / audit target |
| --- | --- | --- | --- | --- |
| `FEATURE_NOTIFICATIONS_ENABLED` | Enables in-app notifications. | `true` | `true` | `false` |
| `FEATURE_MINT_PAGES_ENABLED` | Enables the MINT learning pages. | `true` | `true` | `false` |
| `FEATURE_MULTIPLE_S3_PROVIDERS_ENABLED` | Allows files to use more than one S3 storage provider. | `true` | `true` | `true` |
| `FEATURE_VIDEOCONFERENCE_ENABLED` | Enables video conferences in courses and rooms. | `true` (shared default) | `false` | `true` (shared default) |
| `FEATURE_VIDEOCONFERENCE_WAITING_ROOM_ENABLED` | Enables the waiting room before a video conference. | `true` | `false` | `true` |
| `FEATURE_USER_MIGRATION_ENABLED` | Enables the administrator's user migration tools. | `true` | `false` | `false` |
| `FEATURE_ALERTS_ON_HOMEPAGE_ENABLED` | Shows alerts on the home page. | `false` | `false` | `true` (shared default) |
| `FEATURE_COMMON_CARTRIDGE_COURSE_EXPORT_ENABLED` | Exports courses in Common Cartridge format. | `true` | `true` | `false` |
| `FEATURE_COMMON_CARTRIDGE_COURSE_IMPORT_ENABLED` | Imports courses in Common Cartridge format. | `true` | `false` | `false` |
| `FEATURE_TEAM_CREATE_ROOM_ENABLED` | Lets users create rooms from a team. | `true` | `false` | Not configured by BRB |
| `FEATURE_COLUMN_BOARD_EXTERNAL_TOOLS_ENABLED` | Allows external tools to be added to column boards. | `true` (shared default) | `true` | `true` |
| `FEATURE_MEDIA_SHELF_ENABLED` | Enables media shelf content in column boards. | `true` (shared default) | `true` | `true` |
| `FEATURE_COURSE_SHARE` | Allows courses to be shared. | `true` (shared default) | `false` | `true` (shared default) |
| `FEATURE_LESSON_SHARE` | Allows lessons to be shared. | `true` (shared default) | `false` | `true` (shared default) |
| `FEATURE_TASK_SHARE` | Allows tasks to be shared. | `true` (shared default) | `false` | `true` (shared default) |
| `FEATURE_SCHOOL_DATA_READONLY_ENABLED` | Makes school data read-only in relevant administration flows. | `false` (shared default) | `true` | `true` |
| `FEATURE_TEAMS_INVITE_EXTERNAL_ENABLED` | Controls invitations to teams for external people. | Not configured | `false` | Not configured by BRB |
| `FEATURE_SCHULCONNEX_COURSE_SYNC_ENABLED` | Synchronizes courses through Schulconnex. | `false` (shared default) | `false` | `false` |
| `FEATURE_ROOM_COPY_ENABLED` | Allows rooms to be copied. | `true` (shared default) | `false` | `true` (shared default) |
| `FEATURE_ROOM_SHARE` | Allows rooms to be shared. | `true` (shared default) | `false` | `true` (shared default) |
| `FEATURE_ROOM_ADD_EXTERNAL_PERSONS_ENABLED` | Allows external people to be added to rooms. | `true` (shared default) | `false` | `true` (shared default) |
| `FEATURE_ROOM_REGISTER_EXTERNAL_PERSONS_ENABLED` | Allows external people to register for rooms. | `true` (shared default) | `false` | `true` (shared default) |
| `FEATURE_ROOM_LINK_INVITATION_EXTERNAL_PERSONS_ENABLED` | Allows external people to join rooms through an invitation link. | `true` (shared default) | `false` | `true` (shared default) |
| `FEATURE_EXTERNAL_PERSON_REGISTRATION_ENABLED` | Enables the external-person registration flow. | `true` (shared default) | `false` | `true` (shared default) |
| `FEATURE_OAUTH_LOGIN_ENABLED` | Offers OAuth-based single sign-on. | `false` (shared default) | `false` (shared default) | `false` (shared default) |
| `FEATURE_CONSENT_NECESSARY` | Enables the necessary-consent setting. | `true` (shared default) | `true` (shared default) | `false` |
| `FEATURE_FWU_CONTENT_ENABLED` | Enables FWU media-shelf content. | `false` (shared default) | `false` (shared default) | `true` in BRB; disabled in audit pending preparation |
| `WITH_LDAP` | Includes LDAP integration and sync services. | `true` | `false` | `true` |
| `WITH_COMMON_CARTRIDGE` | Includes Common Cartridge import/export support. | `true` | `true` | `false` (shared default) |
| `WITH_NOTIFICATION_SERVER` | Includes the notification server service. | `true` | `false` | `false` (shared default) |
| `WITH_FWU` | Includes the FWU content service. | `false` (shared default) | `false` (shared default) | `true` in BRB; disabled in audit pending preparation |

The audit configuration deliberately does not copy the pre-SVSDEV-370 DBC feature values. It follows BRB's effective settings except for FWU, which remains disabled until the audit instance is prepared for it. OAuth stays disabled through the shared default; the audit group does not repeat that setting.

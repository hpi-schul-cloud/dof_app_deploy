# Tasks V3 handoff

This document summarizes the current Tasks V3 migration work so it can be continued from another machine.

## Repositories involved

- `nuxt-client`: new task overview, task creation/edit/detail pages, file table integration, feature-flag routing.
- `schulcloud-client`: legacy homework/task pages and the legacy-to-Nuxt redirects.
- `schulcloud-server`: V3 task API and task-description HTML sanitization.
- `file-storage`: existing temporary upload and file-copy/promotion APIs. No new file-storage change is currently required for the task media work.
- `ckeditor`: local custom CKEditor build with task-specific image, audio, and video upload plugins.
- `dof_app_deploy`: feature flag and Kubernetes ingress configuration.

## Feature flag

The flag is:

```text
FEATURE_TASKS_V3_ENABLED
```

Default configuration is enabled in:

```text
ansible/group_vars/all/config.yml
```

Current instance overrides set it to false for:

- `brb`
- `nbc`
- `thr`

`dbc` uses the default true value. The flag is exposed to both server and client configuration.

## Intended routing behavior

`/tasks` always belongs to Nuxt and must remain there, regardless of the flag.

When `FEATURE_TASKS_V3_ENABLED=true`:

- `/tasks` → Nuxt task overview
- `/tasks/new` → Nuxt task creation
- `/tasks/:id` → Nuxt task detail
- `/tasks/:id/edit` → Nuxt task editing
- legacy `/homework/:id` redirects to the corresponding Nuxt task detail unless the submissions tab is requested

When `FEATURE_TASKS_V3_ENABLED=false`:

- `/tasks` → still Nuxt task overview
- `/tasks/new` → `/homework/new?returnUrl=tasks`
- `/tasks/:id` → `/homework/:id`
- `/tasks/:id/edit` → `/homework/:id/edit`

The Nuxt guard only redirects `/tasks/...` subroutes, never `/tasks` itself. The Kubernetes ingress already sends `/tasks` to `nuxtclient-svc`; `/homework` falls through to the legacy `client-svc`. In local development, the Vite proxy sends non-Nuxt routes such as `/homework` to the legacy client on port 3100.

## Current task editor functionality

The Nuxt task editor supports:

- title validation
- course and topic selection
- schedule and submission settings
- draft/private state
- public student submissions setting
- group submissions and maximum group size
- rich text formatting, math, tables, and image resizing
- direct image upload
- direct audio upload
- direct video upload
- normal task attachments through the existing task file table

Inline image/audio/video flow:

1. The user selects a file through a hidden `accept="image/*"`, `accept="audio/*"`, or `accept="video/*"` input.
2. Nuxt uploads it as a temporary user file.
3. CKEditor inserts the temporary download URL into the description.
4. On task save, the task is created/updated first.
5. Referenced temporary media is copied to the task parent.
6. Temporary URLs are replaced with permanent task-file URLs.
7. Temporary files are deleted.

Video currently has basic playback only. Resizing video would require a dedicated CKEditor model/UI plugin; the existing image resize plugin does not apply to video.

## Attachment highlighting

The task attachment table now optionally highlights files referenced in the description with:

```text
Used in task description
```

This is opt-in. `FileTable` has an optional `highlightedFileIds` prop, so other consumers of the shared table are unchanged.

`TaskFiles` parses only `img`, `audio`, and `video` source URLs matching:

```text
/api/v3/file/download/<fileId>/...
```

This is presentation-only and does not change file authorization.

## Important implementation files

### Nuxt client

- `src/router/guards/legacy-route-compatibility.guard.ts`
- `src/router/guards/legacy-route-compatibility.guard.unit.ts`
- `src/router/vue-client-route.ts`
- `src/components/tasks/TaskFiles.vue`
- `src/pages/tasks/TaskOverview.page.vue`
- `src/pages/tasks/TaskEdit.page.vue`
- `src/pages/tasks/TaskDetails.page.vue`
- `src/modules/feature/editor/InlineEditor.vue`
- `src/modules/feature/editor/config.ts`
- `src/modules/feature/folder/file-table/FileTable.vue`
- `src/utils/task-description-files.ts`

### CKEditor

- `src/ckeditor.js`
- `src/plugins/taskimageupload.js`
- `src/plugins/taskaudioupload.js`
- `src/plugins/taskvideoupload.js`
- `src/plugins/video.svg`

The local package is installed into Nuxt from `../ckeditor`. After CKEditor source changes:

```sh
cd ckeditor
npm run build
cd ../nuxt-client
npm install ../ckeditor --no-save --ignore-scripts
```

The Nuxt Dockerfile intentionally uses `npm ci --ignore-scripts`; do not rely on package install scripts.

### Legacy client

- `controllers/homework.js`
- `config/default.schema.json`
- `helpers/handlebars/middleware.js`

The legacy controller uses `Configuration.has('FEATURE_TASKS_V3_ENABLED')` before reading the flag. This was added because the configuration schema must define the key.

### Server

- `apps/server/src/shared/controller/transformer/sanitize-html.transformer.ts`
- `apps/server/src/shared/controller/transformer/sanitize-html.transformer.spec.ts`
- `apps/server/src/modules/task/api/dto/task-create.params.ts`
- `apps/server/src/modules/task/api/dto/task-update.params.ts`

Task rich text allows `img`, `audio`, and `video` only for the task input format. Generic CKEditor rich text does not automatically receive these media tags. Allowed media attributes are restricted to `src`, `controls`, and `controlslist`; task image figure resize styles remain allowed.

## Verification already performed

- CKEditor production build passed.
- Nuxt type-check passed after the attachment highlighting changes.
- Nuxt production build passed, with existing Rollup circular-dependency and large-chunk warnings.
- Nuxt focused file-table and description-parser tests passed.
- Schulcloud-server sanitizer test passed: 20 tests.
- Nuxt task route guard tests cover enabled/disabled behavior and passed.

## Known caveats / next checks

1. Test the feature-flag routing in both a real Kubernetes deployment and local Vite development. Specifically verify `/tasks`, `/tasks/new`, `/tasks/<id>`, and `/tasks/<id>/edit` with the flag false.
2. Verify that `/homework/new?returnUrl=tasks` returns to the Nuxt overview after legacy task creation.
3. Verify the legacy submissions link from a Nuxt task detail page, including `?tab=submissions#activetabid=submissions`.
4. Test attachment highlighting with image, audio, and video files after saving and after renaming an attachment.
5. Test deleting a task with inline media and confirm task file records are deleted by the server/file-storage integration.
6. The working tree contains changes across the repositories listed above. Review each repository separately before committing; do not use destructive cleanup commands because unrelated user changes may be present.


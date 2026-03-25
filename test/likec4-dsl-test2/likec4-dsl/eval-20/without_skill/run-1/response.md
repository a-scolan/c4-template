Use this command:
likec4 validate --config projects/template/likec4.config.json --files projects/template/system-model.c4 projects/template/system-views.c4 --format json --skip-layout-drift

To confirm both files were actually filtered, inspect the JSON and verify that the file-selection/filtered-files section lists exactly these two repository-relative paths: `projects/template/system-model.c4` and `projects/template/system-views.c4`. The safest check is that the filtered/selected file array has length 2 and no other `.c4` source paths appear in the validated input set.

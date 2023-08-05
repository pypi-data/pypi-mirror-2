sync_schema_props_perms('TestExecution', syncperms=False)
sync_schema_props_perms('CheckResultInfo', syncperms=False)
sync_schema_props_perms('use_environment', syncprops=False)
sync_schema_props_perms('local_repository', syncprops=False)
sync_schema_props_perms('needs_checkout', syncprops=False)
add_relation_definition('TestExecution', 'log_file', 'File')
if 'file' in config.cubes():
    sync_schema_props_perms('File', syncprops=False)
else:
    add_cube('file')

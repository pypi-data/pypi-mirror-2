import instances
import utilities as util

# Configure defaults if needed
util.set_default(instances.create, "factory")
util.set_default({}, "constraint_args")
util.set_default({}, "mapper_args")
util.set_default({}, "relationship_args")
util.set_default({}, "table_args")

from motor.motor_asyncio import AsyncIOMotorClient

MONGO_DETAILS = "mongodb://localhost:27017"

client = AsyncIOMotorClient(MONGO_DETAILS)
db = client.assessment_db
employee_collection = db.get_collection("employees")

async def init_db():
    # Add unique index for employee_id
    await employee_collection.create_index("employee_id", unique=True)

    # JSON Schema validation
    validation_schema = {
        "$jsonSchema": {
            "bsonType": "object",
            "required": ["employee_id", "name", "department", "salary", "joining_date", "skills"],
            "properties": {
                "employee_id": {"bsonType": "string"},
                "name": {"bsonType": "string"},
                "department": {"bsonType": "string"},
                "salary": {"bsonType": "number"},
                "joining_date": {"bsonType": "string"},
                "skills": {
                    "bsonType": "array",
                    "items": {"bsonType": "string"}
                }
            }
        }
    }

    # Apply validator
    try:
        await db.command({
            "collMod": "employees",
            "validator": validation_schema,
            "validationLevel": "strict"
        })
    except Exception:
        # If collMod fails (collection not created), create with validator
        await db.create_collection("employees", validator=validation_schema)
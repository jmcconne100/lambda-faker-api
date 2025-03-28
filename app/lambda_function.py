import json
import uuid
import boto3
from faker import Faker

# === Config ===
S3_BUCKET_NAME = "jon-json-test-bucket"

fake = Faker()
s3 = boto3.client("s3")

# === Base Class ===
class FakeDataGenerator:
    def __init__(self):
        self.fake = fake

    def generate(self):
        raise NotImplementedError("Subclasses must implement this method.")

    @classmethod
    def from_json(cls, body):
        try:
            data = json.loads(body)
            data_type = data.get("type", "").lower()

            if data_type == "user":
                return FakeUser().generate()
            elif data_type == "company":
                return FakeCompany().generate()
            else:
                return {"error": "Invalid type. Use 'user' or 'company'."}
        except json.JSONDecodeError:
            return {"error": "Invalid JSON format."}

# === User Generator ===
class FakeUser(FakeDataGenerator):
    def generate(self):
        return {
            "type": "user",
            "name": self.fake.name(),
            "email": self.fake.email(),
            "address": self.fake.address(),
            "phone": self.fake.phone_number(),
            "dob": self.fake.date_of_birth().isoformat()
        }

# === Company Generator ===
class FakeCompany(FakeDataGenerator):
    def generate(self):
        return {
            "type": "company",
            "company_name": self.fake.company(),
            "catch_phrase": self.fake.catch_phrase(),
            "bs": self.fake.bs(),
            "address": self.fake.address(),
            "phone": self.fake.phone_number()
        }

# === S3 Upload Helper ===
def write_to_s3(data, prefix="output"):
    key = f"{prefix}/{uuid.uuid4()}.json"
    try:
        s3.put_object(
            Bucket=S3_BUCKET_NAME,
            Key=key,
            Body=json.dumps(data),
            ContentType="application/json"
        )
        return {"message": "Data written to S3", "s3_key": key}
    except Exception as e:
        return {"error": str(e)}

# === Lambda Handler ===
def lambda_handler(event, context):
    body = event.get("body", "{}")
    result = FakeDataGenerator.from_json(body)
    s3_result = write_to_s3(result)

    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps({
            "data": result,
            "s3": s3_result
        })
    }

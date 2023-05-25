from datetime import datetime
from pymongo import MongoClient
import certifi as certifi
from config import Settings

aa = Settings()
print(aa.MONGO_VAR)



from schemas import Otp, OtpHistory

client = MongoClient(aa.MONGO_VAR,
                     tlsCAFile=certifi.where())

db = client.Fast  # database name
otpCollection = db.FastAPICollection  # collection name


def status_check():
    otps = otpCollection.find({"currentStatus": 0})
    otps_as_list = list(otps)
    print(f"Total {len(otps_as_list)}")
    skipped = 0
    updated = 0

    for otp in otps_as_list:
        otpModel = Otp(**otp)
        print(otp['expiryOn'])
        if otp['expiryOn'] < datetime.now():
            otp_History = OtpHistory(
                stateId=2,
                stateDescription="OTP Expired",
                stateDate=datetime.now()
            )
            otpModel.stateHistory.append(otp_History)
            otpModel.currentStatus = 2
            otpCollection.update_one({"genId": otp['genId']}, {"$set": otpModel.dict()})

            updated += 1
            print(f"Updated {otp['genId']}")
        else:
            print(f"Skipped {otp['genId']}")
            skipped += 1

    print(f"Updated {updated} and Skipped {skipped}")


status_check()

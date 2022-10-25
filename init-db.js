db = db.getSiblingDB("users_db");
db.users_tb.drop();

db.users_tb.insertMany([
    {
        "name": "user1",
        "password": "pwd1"
    },
    {
        "name": "user2",
        "password": "pwd2"
    }
]);
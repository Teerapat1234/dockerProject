CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE IF NOT EXISTS "Restaurant" (
    "id" UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    "name" TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS "Food" (
   "id" SERIAL PRIMARY KEY,
   "name" TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS "Time" (
   "id" SERIAL PRIMARY KEY,
   "name" TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS "RestaurantMenu" (
    "restaurantId" UUID NOT NULL REFERENCES "Restaurant" ("id"),
    "FoodId" INT NOT NULL REFERENCES "Food" ("id"),
    "TimeId" INT NOT NULL REFERENCES "Time" ("id")
);

SELECT * FROM "RestaurantMenu";
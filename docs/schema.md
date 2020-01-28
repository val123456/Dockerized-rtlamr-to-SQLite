```sql
BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "Gas_DailyUse_44448439" (
	"id"	integer,
	"date"	text,
	"time"	text,
	"ccf"	real,
	"fulldatetime"	text,
	PRIMARY KEY("id")
);
CREATE TABLE IF NOT EXISTS "Gas_Meter_44448439" (
	"id"	integer,
	"date"	text,
	"time"	text,
	"ccf"	real,
	"fulldatetime"	text,
	PRIMARY KEY("id")
);
CREATE TABLE IF NOT EXISTS "Water_DailyUse_1563476986" (
	"id"	integer,
	"date"	text,
	"time"	text,
	"cuft"	real,
	"fulldatetime"	text,
	PRIMARY KEY("id")
);
CREATE TABLE IF NOT EXISTS "Water_Meter_1563476986" (
	"id"	integer,
	"date"	text,
	"time"	text,
	"cuft"	real,
	"fulldatetime"	text,
	PRIMARY KEY("id")
);
CREATE TABLE IF NOT EXISTS "Electric_DailyUse_22277181" (
	"id"	integer,
	"date"	text,
	"time"	text,
	"kWHs"	real,
	"fulldatetime"	text,
	PRIMARY KEY("id")
);
CREATE TABLE IF NOT EXISTS "Electric_Meter_22277181" (
	"id"	integer,
	"date"	text,
	"time"	text,
	"kWHs"	real,
	"fulldatetime"	text,
	PRIMARY KEY("id")
);
CREATE TABLE IF NOT EXISTS "Electric_DailyUse_629848" (
	"id"	integer,
	"date"	text,
	"time"	text,
	"kWHs"	real,
	"fulldatetime"	text,
	PRIMARY KEY("id")
);
CREATE TABLE IF NOT EXISTS "Electric_Meter_629848" (
	"id"	integer,
	"date"	text,
	"time"	text,
	"kWHs"	real,
	"fulldatetime"	text,
	PRIMARY KEY("id")
);
CREATE INDEX IF NOT EXISTS "index_use_44448439" ON "Gas_DailyUse_44448439" (
	"date"
);
CREATE INDEX IF NOT EXISTS "index_44448439" ON "Gas_Meter_44448439" (
	"date"
);
CREATE INDEX IF NOT EXISTS "index_use_1563476986" ON "Water_DailyUse_1563476986" (
	"date"
);
CREATE INDEX IF NOT EXISTS "index_1563476986" ON "Water_Meter_1563476986" (
	"date"
);
CREATE INDEX IF NOT EXISTS "index_use_22277181" ON "Electric_DailyUse_22277181" (
	"date"
);
CREATE INDEX IF NOT EXISTS "index_22277181" ON "Electric_Meter_22277181" (
	"date"
);
CREATE INDEX IF NOT EXISTS "index_use_629848" ON "Electric_DailyUse_629848" (
	"date"
);
CREATE INDEX IF NOT EXISTS "index_629848" ON "Electric_Meter_629848" (
	"date"
);
COMMIT;
```
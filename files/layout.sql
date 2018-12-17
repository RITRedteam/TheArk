-- These are the servers that we know about
CREATE TABLE `servers` (
	`server_name`		TEXT,
	`server_url`	    TEXT,
	`creation_date`	    TEXT
);

-- This table holds all of the assigned ip address and the interface they are mapped to if applicable
CREATE TABLE `ips` (
	`server_name`		TEXT NOT NULL,
	`address`			TEXT NOT NULL,
	`interfacename`		TEXT
);


-- This table holds all the ip addresses that we know of that are not currently in use
CREATE TABLE `available_ips` (
	`ip`				TEXT
)
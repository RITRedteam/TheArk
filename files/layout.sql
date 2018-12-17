-- These are the servers that we know about
CREATE TABLE `servers` (
	`server_name`		TEXT,
	`server_type`		TEXT,
	`assign_addresses`	BOOLEAN,
	`creation_date`	    TEXT
);

-- This table hold information for redirect servers
CREATE TABLE `server_redirects` (
	`server_name`		TEXT,
	`server_http_url`	TEXT,
	`server_tcp_url`	TEXT,
	`server_http_path`	TEXT
);

-- Hold all the TCP ports to be forwarded for a server
CREATE TABLE `server_ports` (
	`server_name`		TEXT,
	`port`				INT
);

-- This table holds all of the assigned ip address and the interface they are mapped to if applicable
CREATE TABLE `ips` (
	`server_name`		TEXT,
	`address`			TEXT,
	`interfacename`		TEXT
);


-- This table holds all the ip addresses that we know of that are not currently in use
CREATE TABLE `available_ips` (
	`ip`				TEXT
)
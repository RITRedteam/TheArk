# The Ark
The Ark manages virtual IP addresses for redteam tools. It can spin up NGINX server blocks to listen on for upstreaming to redteam servers and C2s. The Ark is also responsible for being the single source of truth for which virtual IPs are assigned to what redteam tools. Tools can request a list of virtual IP addressses to have reserved (for example, [Sangheili](https://github.com/RITRedteam/Sangheili) can request a list of IPs to use for outgoing connections). Because the mappings need to be persistent, The Ark writes the mappings to a Sqlite3 database.

## Documentation
Im trying hard to document the code and document the API and usage and such. You can read all the documentation [here](./docs/README.md)

## Contributing
If you want to work on this, just follow the TODOs for now
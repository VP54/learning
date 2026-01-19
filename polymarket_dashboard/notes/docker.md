# Docker
- To create a Quest DB use: `docker compose up`


## Commands

- `depends_on` controls startup order not actually waiting service that its started
  - Has to be solved explicitly
- `volumes` specifies: `<path locally>:<path in your container>`
- `include` includes another service(s) from another `.yml`
  - Something like:
      ```yaml 
        # infa.yaml
        services:
          redis:
            ...
        
        # compose.yaml
        include:
          infra.yaml
        
        services:
          mongo-db:
            ...
      ```


## Ports:
- `srtartport:endport/protocol` - if no protocol then TCP is used

## Volumes:

## HOw compose works under the hood

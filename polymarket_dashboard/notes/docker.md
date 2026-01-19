# Docker Compose
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
- `secrets` - adds location of secrets
  ```yaml
  services:
  myapp:
    image: myapp:latest
    secrets:
      - my_secret
  secrets:
    my_secret:
      file: ./my_secret.txt
  ```


## Ports:
- `srtartport:endport/protocol` - if no protocol then TCP is used

## Volumes:
- persistent data stores
- named volumes can be reused across services
    - In the following example db-data is copied to `/etc/data` and `/var/lib/backup/data`
    ```yaml
    services:
      backend:
        image: example/database
        volumes:
          - db-data:/etc/data
  
      backup:
        image: backup-service
        volumes:
          - db-data:/var/lib/backup/data
  
    volumes:
      db-data:
    ```
    - Parameter `external` specifies volume that is managed outside of the application
       ```yaml
       services:
         backend:
           image: example/database
           volumes:
             - db-data:/etc/data

       volumes:
         db-data:
           external: true
       ```

## Profiles
- I can define active profiles so that app is adjusted for various usages.
  - To run: `docker compose --profile test --profile debug up` (You can run multiple profiles)
  - If I run some profile that depends_on the other
  - **Example**:
    ```yaml
    services:
      web:
        image: web_image

      test_lib:
        image: test_lib_image
        profiles:
          - test

      coverage_lib:
        image: coverage_lib_image
        depends_on:
          - test_lib
        profiles:
          - test

      debug_lib:
        image: debug_lib_image
        depends_on:
          - test_lib
        profiles:
          - debug
    ```

## How to build from Dockerfile

**Here:**
  ```yaml
  version: '2'

  services:
    es-master:
      build: ./elasticsearch
      image: porter/elasticsearch
      ports:
        - "9200:9200"
      container_name: es_master

    es-node:
      image: porter/elasticsearch
      depends_on:
        - es-master
      ports:
        - "9200"
      command: elasticsearch --discovery.zen.ping.unicast.hosts=es_master
  ```
  - image for es-master service is located in `./elasticseaerch`
  - its name is tagged to: `porter/elasticsearch`
  - then `es-node` is based on `porter/elasticsearch` (which is the previously built)


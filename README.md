# ZX Play API for Z88DK

## Development start

### Initial project setup

```bash
git clone git@git.tiepy.dev:zxplay/zxplay-api-z88dk.git
cd zxplay-api-z88dk/
virtualenv venv
source ./venv/bin/activate
pip install -r requirements.txt
```

### Run app

```bash
uvicorn app.main:app --reload
```

## Docker Build & Push

```bash
docker build -t steverobertson/zxplay-api-z88dk .
docker push steverobertson/zxplay-api-z88dk
```

## Run Locally

```bash
docker run \
  --publish=80:8000 \
  --detach=true \
  --name=zxplay-api-z88dk \
  steverobertson/zxplay-api-z88dk
```

## Hasura Deployment Configuration

### Compile Action Service

Tick option to "Forward client headers to webhook".

#### Action definition

```graphql
type Mutation {
  compileC (
    code: String!
  ): CompileResult
}
```

#### New types definition

```graphql
type CompileResult {
  base64Encoded: String!
}
```

#### Handler

```
http://z88dk/compile/
```

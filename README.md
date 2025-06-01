# Zadanie 2 – Programowanie Aplikacji w Chmurze Obliczeniowej (PAwChO)

## Sekrety używane w workflow

W repozytorium ustawione są następujące sekrety (Settings > Secrets and variables > Actions):

| Nazwa               | Opis                                                |
|---------------------|-----------------------------------------------------|
| `GHCR_USERNAME`     | Login GitHub                                        |
| `GHCR_TOKEN`        | GitHub Personal Access Token (write:packages etc.)  |
| `DOCKERHUB_USERNAME`| Login do DockerHub                                  |
| `DOCKERHUB_TOKEN`   | Access Token z DockerHub                            |

## Etapy działania workflowa

Plik: `.github/workflows/build.yml`

1. Checkout repozytorium
2. Logowanie do DockerHub i GHCR
3. Budowanie lokalnego obrazu `weather-app:test` (tylko `amd64`)
4. Skan obrazu za pomocą Trivy (docker run)
5. Jeżeli brak CVE typu HIGH/CRITICAL – budowa i push multiarch (`amd64`, `arm64`) do GHCR

## Tagowanie obrazów

- Tymczasowy tag lokalny: `weather-app:test` (do skanowania)
- Docelowy obraz multiarch: `ghcr.io/ghcr_username/weather-app:latest`

## Skanowanie bezpieczeństwa – Trivy

Wykonywany jest lokalnie poprzez kontener:
"docker run --rm \
          -v /var/run/docker.sock:/var/run/docker.sock \
          aquasec/trivy:0.50.1 image \
          --severity CRITICAL,HIGH \
          --ignore-unfixed \
          --format table \
          --vuln-type os,library \
          --exit-code 1 \
          weather-app:test"

Jeśli Trivy wykryje CVE typu CRITICAL lub HIGH, pipeline kończy się błędem i obraz nie zostaje wypchnięty.
Pipeline uruchamia się automatycznie przy pushu do `main`.  
Obraz publikowany jest wyłącznie po pozytywnym wyniku skanowania.  

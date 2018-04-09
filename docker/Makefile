# If the first argument is "run"...
# ifeq (cli,$(firstword $(MAKECMDGOALS)))
#  # use the rest as arguments for "run"
#  RUN_ARGS := $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))
#  # ...and turn them into do-nothing targets
#  $(eval $(RUN_ARGS):;@:)
#endif

reset: clean
	sudo rm -rf bitcoind/data
start:
	docker-compose up
clean:
	docker-compose rm pymi_bitcoind
build:
	docker-compose build
cli:
	docker exec -ti docker_pymi_bitcoind_1 bitcoin-cli $(filter-out $@,$(MAKECMDGOALS))


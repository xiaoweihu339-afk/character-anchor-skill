.PHONY: validate compile demo init-example

CHARACTER ?= characters/mira-vale
REQUEST ?= Mira walks through a rain-soaked train station at night, holding her notebook.
PROVIDER ?= provider-neutral

validate:
	python scripts/validate_character_anchor.py $(CHARACTER)

compile:
	python scripts/compile_prompt.py $(CHARACTER) --request "$(REQUEST)" --provider $(PROVIDER)

demo: validate compile

init-example:
	python scripts/init_character_anchor.py --root . --character-id example-character --display-name "Example Character"

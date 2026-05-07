.PHONY: validate compile demo init-example coverage gallery face-lock-dry-run golden-request feedback-dry-run

CHARACTER ?= characters/mira-vale
REQUEST ?= Mira walks through a rain-soaked train station at night, holding her notebook.
PROVIDER ?= provider-neutral
GALLERY_OUTPUT ?= outputs/tmp/review-gallery.html

validate:
	python scripts/validate_character_anchor.py $(CHARACTER)

compile:
	python scripts/compile_prompt.py $(CHARACTER) --request "$(REQUEST)" --provider $(PROVIDER)

coverage:
	python scripts/audit_media_coverage.py $(CHARACTER)

gallery:
	python scripts/build_review_gallery.py $(CHARACTER) --output $(GALLERY_OUTPUT)

face-lock-dry-run:
	python scripts/update_face_lock.py $(CHARACTER) --measurement eye_spacing_ratio=1.0 --qualitative-lock "moderate eye spacing" --dry-run

golden-request:
	python scripts/generate_golden.py $(CHARACTER) --request "$(REQUEST)" --provider $(PROVIDER)

feedback-dry-run:
	python scripts/record_golden_feedback.py $(CHARACTER) --candidate-id demo-candidate --user-rating 4 --liked-point "stable face direction" --dry-run

demo: validate compile

init-example:
	python scripts/init_character_anchor.py --root . --character-id example-character --display-name "Example Character"

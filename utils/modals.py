absmodal = interactions.Modal(
            title="Absence",
            custom_id="abs_requests",
            components=[
                interactions.TextInput(
                    style=interactions.TextStyleType.PARAGRAPH,
                    label="Raison d'absence",
                    custom_id="abs_requests_reason",
                    placeholder="Veuillez entrer la raison ici.",
                    required=True,
                ),

                interactions.TextInput(
                    style=interactions.TextStyleType.SHORT,
                    label="Veuillez entrer la date de votre départ.",
                    custom_id="abs_requests_depart_date",
                    placeholder="Sous le format DD/MM/YYYY",
                    min_length=10,
                    max_length=10,
                    required=True,
                ),

                interactions.TextInput(
                    style=interactions.TextStyleType.SHORT,
                    label="Veuillez entrer la date de votre retour.",
                    custom_id="abs_requests_retour_date",
                    placeholder="Sous le format DD/MM/YYYY",
                    min_length=10,
                    max_length=10,
                    required=True,
                ),
            ],
        )


prmodal = interactions.Modal(

            title="Presence Réduite",

            custom_id="pr_modal",

            components=[
                interactions.TextInput(
                    style=interactions.TextStyleType.PARAGRAPH,
                    label="Raison de présence réduite.",
                    custom_id="pr_modal_reason",
                    placeholder="Veuillez entrer la raison ici.",
                    required=True,
                ),

                interactions.TextInput(
                    style=interactions.TextStyleType.SHORT,
                    label="Veuillez entrer la date de votre départ.",
                    custom_id="pr_modal_depart",
                    placeholder="Sous le format DD/MM/YYYY",
                    min_length=10,
                    max_length=10,
                    required=True,
                ),

                interactions.TextInput(
                    style=interactions.TextStyleType.SHORT,
                    label="Veuillez entrer la date de votre retour.",
                    custom_id="pr_modal_retour",
                    placeholder="Sous le format DD/MM/YYYY",
                    min_length=10,
                    max_length=10,
                    required=True,

                ),

            ],

        )
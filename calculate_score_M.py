from services.hydra_rules_service import HydraRulesService
from columns_keys import (
    COLUMN_BASAL_DISC,
    COLUMN_MOUNTH,
    COLUMN_NUMBER_TOTAL_OF_TENTACLES,
    COLUMN_START_TENTACLES
)


class GenerateScoreM:
    sheet = None
    hydra_rules_service: HydraRulesService | None = None

    def __init__(self, sheet):
        self.sheet = sheet
        self.hydra_rules_service = HydraRulesService()

    def _calculate_score_in_six_to_ten_range(
        self,
        tentacles_surpass_half_body: int,
        has_started_tentacles: bool,
        has_more_tentacles: bool
    ) -> float:

        base_scores: dict[int, int] = {
            0: 6,
            1: 7,
            2: 8,
            3: 9
        }

        tentacles_up_and_surpassing = (
            has_more_tentacles and tentacles_surpass_half_body == 0
        )
        tentacles_creation_finished = (
            has_started_tentacles and not has_more_tentacles
        )

        if tentacles_creation_finished or tentacles_up_and_surpassing:
            score = base_scores[0]
        elif tentacles_surpass_half_body in base_scores:
            score = base_scores[tentacles_surpass_half_body]
        elif tentacles_surpass_half_body >= 4:
            return 10

        return score

    def get_score_M(self, row: int, tentacles_surpass_half_body: int) -> float:
        cell_D = self.sheet.cell(row=row, column=COLUMN_MOUNTH).value
        cell_E = self.sheet.cell(row=row, column=COLUMN_BASAL_DISC).value
        cell_F = self.sheet.cell(row=row, column=COLUMN_START_TENTACLES).value
        cell_M = self.sheet.cell(
            row=row,
            column=COLUMN_NUMBER_TOTAL_OF_TENTACLES
        ).value

        hydra_not_have_mouth = self.hydra_rules_service.hydra_not_have_mouth(
            cell_D
        )
        has_more_tentacles = self.hydra_rules_service.has_more_tentacles(
            cell_M
        )

        base_score = self.hydra_rules_service.calculate_score_base_conditions(
            self.sheet,
            row
        )
        if base_score is not None:
            return base_score

        is_hydra_complete = self.hydra_rules_service.is_hydra_complete(
            self.sheet,
            row,
            tentacles_surpass_half_body
        )

        has_started_tentacles = cell_F == 1
        has_basal_disc_without_tentacles = not hydra_not_have_mouth and cell_E == 1
        has_basal_with_started_tentacles = (
            has_basal_disc_without_tentacles and not has_started_tentacles and cell_M == 0
        )

        if is_hydra_complete or has_basal_with_started_tentacles:
            return 5
        elif has_basal_disc_without_tentacles:
            return self._calculate_score_in_six_to_ten_range(
                tentacles_surpass_half_body=tentacles_surpass_half_body,
                has_more_tentacles=has_more_tentacles,
                has_started_tentacles=has_started_tentacles
            )

        return None

from services.hydra_rules_service import HydraRulesService
from columns_keys import (
    COLUMN_BASAL_DISC,
    COLUMN_MOUNTH,
    COLUMN_NUMBER_TOTAL_OF_TENTACLES,
    COLUMN_START_TENTACLES
)


class GenerateScoreI:
    sheet = None
    hydra_rules_service: HydraRulesService | None = None

    def __init__(self, sheet):
        self.sheet = sheet
        self.hydra_rules_service = HydraRulesService()

    def _calculate_score_in_six_to_ten_range(
        self,
        total_tentacles_upper_half_long_body: int,
        has_more_tentacles: bool,
        has_started_tentacles: bool,
    ) -> int:

        tentacles_up_and_surpassing = (
            has_more_tentacles and total_tentacles_upper_half_long_body == 0
        )
        tentacles_creation_finished = (
            has_started_tentacles and not has_more_tentacles
        )

        if tentacles_up_and_surpassing or tentacles_creation_finished:
            return 6
        if total_tentacles_upper_half_long_body == 1:
            return 7
        if total_tentacles_upper_half_long_body in (2, 3):
            return 8
        if total_tentacles_upper_half_long_body >= 4:
            return 10

        return 0

    def get_score_I(
        self,
        row: int,
        total_tentacles_upper_half_long_body: int
    ) -> float:
        """_summary_
        Args:
            total_tentacles_sup (int): Is a total_tentacles_sup of a long body(Column N) or number tentacles a mid body

        Returns:
            float: score of row
        """

        cell_D = self.sheet.cell(row=row, column=COLUMN_MOUNTH).value
        cell_E = self.sheet.cell(row=row, column=COLUMN_BASAL_DISC).value
        cell_F = self.sheet.cell(row=row, column=COLUMN_START_TENTACLES).value
        cell_M = self.sheet.cell(row=row, column=COLUMN_NUMBER_TOTAL_OF_TENTACLES).value

        hydra_not_have_mouth: bool = self.hydra_rules_service.hydra_not_have_mouth(
            cell_D
        )
        has_more_tentacles: bool = self.hydra_rules_service.has_more_tentacles(
            cell_M
        )

        has_basal_disc: bool = self.hydra_rules_service.has_basal_disc(
            cell_D,
            cell_E,
            cell_F
        )

        cell_F = self.sheet.cell(row=row, column=COLUMN_START_TENTACLES).value

        score = self.hydra_rules_service.calculate_score_base_conditions(
            self.sheet,
            row,
        )

        if score is not None:
            return score
        elif has_basal_disc and has_more_tentacles and total_tentacles_upper_half_long_body == 0:
            score = 5
        # Default cell_D = 1 and cell_E = 1 and cell_F = 0 for a score sup a 5
        elif not hydra_not_have_mouth and cell_E == 1:
            score = self._calculate_score_in_six_to_ten_range(
                total_tentacles_upper_half_long_body=total_tentacles_upper_half_long_body,
                has_more_tentacles=has_more_tentacles,
                has_started_tentacles=cell_F == 1
            )

        return score

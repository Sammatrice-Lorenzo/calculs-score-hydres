from services.hydra_rules_service import HydraRulesService
from columns_keys import (
    COLUMN_BASAL_DISC,
    COLUMN_MOUNTH,
    COLUMN_NUMBER_TOTAL_OF_TENTACLES,
    COLUMN_START_TENTACLES
)


class GenerateScoreTOrE:
    sheet = None
    hydra_rules_service: HydraRulesService | None = None

    def __init__(self, sheet):
        self.sheet = sheet
        self.hydra_rules_service = HydraRulesService()

    def _calculate_score_in_six_to_ten_range(
        self,
        column_comparaison: int,
        total_tentacles_upper: int,
        has_more_tentacles: bool
    ) -> float:

        is_above_average_body: bool = (
            self.hydra_rules_service.is_above_average_body(column_comparaison)
        )

        base_scores: dict[int, int] = {
            0: 6,
            1: 7,
            2: 8,
            3: 8
        }

        if has_more_tentacles and total_tentacles_upper == 0:
            score = base_scores[0]
        elif total_tentacles_upper in base_scores:
            score = base_scores[total_tentacles_upper]
        elif total_tentacles_upper >= 4:
            return 10 if is_above_average_body else 9

        return score + 0.5 if is_above_average_body else score

    def get_score_T_or_E(
        self,
        row: int,
        total_tentacles_upper: int,
        column_comparaison: int
    ) -> float:
        cell_D = self.sheet.cell(row=row, column=COLUMN_MOUNTH).value
        cell_E = self.sheet.cell(row=row, column=COLUMN_BASAL_DISC).value
        cell_F = self.sheet.cell(row=row, column=COLUMN_START_TENTACLES).value
        cell_M = self.sheet.cell(
            row=row,
            column=COLUMN_NUMBER_TOTAL_OF_TENTACLES
        ).value

        if None in (cell_D, cell_E, cell_F, cell_M):
            raise Exception(f"Problème sur la ligne {row}")

        hydra_not_have_mouth: bool = (
            self.hydra_rules_service.hydra_not_have_mouth(cell_D)
        )
        has_more_tentacles: bool = self.hydra_rules_service.has_more_tentacles(
            cell_M
        )

        has_basal_disc: bool = self.hydra_rules_service.has_basal_disc(
            cell_D,
            cell_E,
            cell_F
        )

        score = self.hydra_rules_service.calculate_score_base_conditions(
            self.sheet,
            row,
        )

        if score is not None:
            return score
        elif has_basal_disc and has_more_tentacles and total_tentacles_upper == 0:
            score = 5
        # Default cell_D = 1 and cell_E = 1 and cell_F = 0 for a score sup a 5
        elif not hydra_not_have_mouth and cell_E == 1 and cell_F == 0:
            score = self._calculate_score_in_six_to_ten_range(
                column_comparaison,
                total_tentacles_upper,
                has_more_tentacles
            )

        return score

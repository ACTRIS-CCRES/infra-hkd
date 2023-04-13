from grafanalib.core import (
    Target,
    AlertRulev9,
)

class AlertRulev9Fixed(AlertRulev9):
    """Implements open PR 
    https://github.com/weaveworks/grafanalib/pull/544/files#diff-e183577edc3e65361ecd131b1d852e4b241b30f61edd379a745317aa49502339
    """
    def to_json_data(self):
        data = []

        for trigger in self.triggers:
            if isinstance(trigger, Target):
                target = trigger
                data += [{
                    "refId": target.refId,
                    "relativeTimeRange": {
                        "from": self.timeRangeFrom,
                        "to": self.timeRangeTo
                    },
                    "datasourceUid": target.datasource,
                    "model": target.to_json_data(),
                }]
            else:
                data += [trigger.to_json_data()]

        return {
            "uid": self.uid,
            "for": self.evaluateFor,
            "labels": self.labels,
            "annotations": self.annotations,
            "grafana_alert": {
                "title": self.title,
                "condition": self.condition,
                "data": data,
                "no_data_state": self.noDataAlertState,
                "exec_err_state": self.errorAlertState,
            },
        }
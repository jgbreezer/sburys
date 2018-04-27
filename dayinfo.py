# Python 2 or Python 3
import csv

# Describe expected outputs for each day declaratively
DAY_ORDER = ["mon", "tue", "wed", "thu", "fri"]

DAY_OUTPUTS = {
    # day: day_process key also matching name of field for output dict
    "mon": "square",
    "tue": "square",
    "wed": "square",
    "thu": "double",
    "fri": "double",
}

DAY_PROCESS = {
    "double": lambda x: x * 2,
    "square": lambda x: x * x,
}

class DayValue:
    process_days = set(DAY_ORDER)

    def __init__(self, file_stream):
        self.open_csv(file_stream)

    def open_csv(self, file_stream):
        self.day_fields = {}
        dow_checks = set()
        self.day_csv = csv.DictReader(file_stream)
        if "description" not in self.day_csv.fieldnames:
            raise KeyError("Missing description column in csv")
        for heading in self.day_csv.fieldnames:
            fields = heading.split("-",1)
            if len(fields) > 1:
                if len(fields) > 2:
                    raise ValueError("Only start and end day allowed in csv range column ({!r})".format(heading))
                # Raises if day unknown/not in lower-case, caller must manage.
                try:
                    field1_index = DAY_ORDER.index(fields[0])
                    field2_index = DAY_ORDER.index(fields[1])
                except:
                    # skip unknown column name
                    fields = None
                    # (handling not in spec, todo: check with client if behaviour is suitable)
                else:
                    # Assumes field title in increasing time order.
                    # Keeping keys as names of days for ease using names in final
                    # output dict instead of index into DAY_ORDER.
                    fields = [DAY_ORDER[i] for i in range(field1_index, field2_index+1)]
                    # Track days included for checks.
                    # Doesn't check for duplicate column/colliding ranges.
                    dow_checks.update(set(fields))
            elif fields[0] in self.process_days:
                # Only update with processed day columns.
                dow_checks.add(fields[0])
            else:
                fields = None

            if fields:
                try:
                    # Ignores duplicate fields/overlapping ranges; last one processed wins.
                    self.day_fields[heading].extend(fields)
                except KeyError:
                    self.day_fields[heading] = fields
        # Check here not in read_row() for missing days or description column.
        if len(dow_checks) < 5:
            raise KeyError("Missing day of the week column(s) in csv")


    def week_values(self):
        for row in self.day_csv:
            week_day_values = {}
            for field, days in self.day_fields.items():
                value = int(row[field])
                for day in days:
                    week_day_values[day] = value
            day_values = []
            for day in DAY_ORDER:
                process = DAY_OUTPUTS[day]
                value = week_day_values[day]
                processed_value = DAY_PROCESS[process](value)
                day_value = {
                    "day": day,
                    "description": "{} {}".format(row["description"], processed_value),
                    process: processed_value,
                    "value": value,
                }
                day_values.append(day_value)

            yield day_values

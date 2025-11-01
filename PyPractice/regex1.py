import re

def main():
    print(convert(input("Hours: ")))

def convert(s):
    try:
        timingsDict = {}

        s = str(s).strip()
        time = re.search(r"^(\d{1,2}|\d{1,2}\:\d{2})\s+(AM|PM) to (\d{1,2}|\d{1,2}\:\d{2})\s+(AM|PM)$", s)
        index = 0

        if not time:
            raise ValueError


        for group in time.groups():
            if group and ':' in group:
                hours, minutes = group.split(':')
            elif group.isdigit():
                hours = group
                minutes = f"00"
            else:
                continue
            hours = int(hours)
            minutes = int(minutes)

            if hours > 12 or minutes > 59:
                raise ValueError
            elif hours == 12:
                hours = 0
            timingsDict[index] = {
                    "hours": f"{hours:02}",
                    "minutes": f"{minutes:02}",
                }

            index += 1

        if time.group(2) == "AM":
            timingsDict.update({1: {"hours": f"{hours + 12}", "minutes": f"{minutes:02}"}})
        elif time.group(2) == "PM":
            timingsDict.update({0: {"hours": f"{hours + 12}", "minutes": f"{minutes:02}"}})
        return f"{timingsDict[0]['hours']}:{timingsDict[0]['minutes']} to {timingsDict[1]['hours']}:{timingsDict[1]['minutes']}"

    except:
        raise ValueError
if __name__ == "__main__":
    main()

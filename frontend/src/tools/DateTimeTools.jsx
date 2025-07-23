// DateTimeTools: Class for handling with datetime
export class DateTimeTools {
    static momentToStr(datetime, format="YYYY-MM-DDTHH:mm:ss") {
        return datetime.format(format);
    }
}
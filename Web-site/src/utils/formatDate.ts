import { languageLocales } from "@/utils/languageLocales.js";

export function formatDate(date: string) {
    const dateObj: Date = new Date(date);
  
    // Format the date as desired
    const formattedDate: string = dateObj.toLocaleDateString(
      languageLocales[document.documentElement.getAttribute("lang") || "en"],
      {
        weekday: "short",
        day: "2-digit",
        month: "short",
        year: "numeric"
      }
    );
    return formattedDate;
  }
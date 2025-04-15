/**
 * Function provided by deepseek.ai 8b model + ollama, with some minor
 * tweaks, i.e., defensive coding w.r.t. `futureDate`).
 */

function calculateTimeDifference(futureDate) {
    // Get current timestamp
    const now = new Date();
    const currentTime = now.getTime();

    if (typeof futureDate === 'undefined') {
      return "";
    }

    // Get future timestamp
    const futureTimestamp = futureDate.getTime();

    // Calculate difference in milliseconds
    const differenceMs = futureTimestamp - currentTime;

    // Convert to seconds
    const differenceSeconds = Math.floor(differenceMs / 1000);

    // Calculate individual components
    const days = Math.floor(differenceSeconds / (24 * 60 * 60));
    const hoursRemaining = differenceSeconds % (24 * 60 * 60);
    const hours = Math.floor(hoursRemaining / (60 * 60));
    const minutesRemaining = hoursRemaining % (60 * 60);
    const minutes = Math.floor(minutesRemaining / 60);
    const seconds = Math.floor((differenceMs % 1000) / 1000);

    // Format the string
    let timeString = '';
    if (days > 0) {
        timeString += `${days} day${days !== 1 ? 's' : ''} `;
    }
    if (hoursRemaining > 0) {
        timeString += `${hours} hour${hours !== 1 ? 's' : ''} `;
    }
    if (minutesRemaining > 0) {
        timeString += `${minutes} minute${minutes !== 1 ? 's' : ''} `;
    }
    if (seconds > 0) {
        timeString += `${seconds} second${seconds !== 1 ? 's' : ''}`;
    }

    return timeString;
}

const us2026MidtermsDate = new Date(Date.UTC(2026, 11 - 1, 7));
const us2028GeneralElection = new Date(Date.UTC(2028, 11 - 1, 7));

function doGet() {
  let datesToReport = "Times reported below are in UTC.\n";
  datesToReport += "2026 midterms: " + calculateTimeDifference(us2026MidtermsDate) + "\n";
  datesToReport += "2028 general: " + calculateTimeDifference(us2028GeneralElection) + "\n";
  return ContentService.createTextOutput(datesToReport).setMimeType(ContentService.MimeType.TEXT);
}

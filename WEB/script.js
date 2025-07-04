// =============================================
//  ฟังก์ชันดึงข้อมูล 1 ชั่วโมงล่าสุด
// =============================================
async function fetch1hData() {
    try {
        const response = await fetch('http://127.0.0.1:8000/average_pm_data_1h');
        const data = await response.json();

        if (!data || data.error) {
            console.error("❌ No 1-hour average data available.");
            return;
        }

        // ✅ ตรวจสอบค่า และปรับทศนิยมเป็น 2 ตำแหน่ง
        const temperature = data.temperature !== "N/A" && data.temperature !== null ? `${parseFloat(data.temperature).toFixed(2)}°C` : "N/A°C";
        const humidity = data.humidity !== "N/A" && data.humidity !== null ? `${parseFloat(data.humidity).toFixed(2)}%` : "N/A%";
        const pm2_5 = data.pm2_5 !== "N/A" && data.pm2_5 !== null ? parseFloat(data.pm2_5).toFixed(2) : "N/A";
        const pm0_1 = data.pm0_1_predicted !== "N/A" && data.pm0_1_predicted !== null ? parseFloat(data.pm0_1_predicted).toFixed(2) : "N/A";

        // ✅ อัปเดตค่า PM2.5 และ PM0.1 ใน HTML
        document.getElementById("pm25_1h").innerText = `${pm2_5} mg/m³`;
        document.getElementById("pm01_1h").innerText = `${pm0_1} mg/m³`;
        document.getElementById("temperature_1h").innerText = `${temperature}`;
        document.getElementById("humidity_1h").innerText = `${humidity}`; 

        // ✅ อัปเดตสถานะ PM2.5
        if (pm2_5 !== "N/A") {
            const { status, icon } = getPM25Status(parseFloat(pm2_5));
            document.getElementById("status_pm25_text_1h").innerText = status;
            document.getElementById("status_pm25_icon_1h").src = icon;
        }

        // ✅ อัปเดตสถานะ PM0.1
        if (pm0_1 !== "N/A") {
            const { status, icon } = getPM01Status(parseFloat(pm0_1));
            document.getElementById("status_pm01_text_1h").innerText = status;
            document.getElementById("status_pm01_icon_1h").src = icon;
        }

    } catch (error) {
        console.error("❌ Error fetching 1-hour data: ", error);
    }
}

// =============================================
//  ฟังก์ชันดึงข้อมูล 24 ชั่วโมงล่าสุด
// =============================================
async function fetch24hData() {
    try {
        const response = await fetch('http://127.0.0.1:8000/average_pm_data_24h');
        const data = await response.json();

        if (!data || data.error) {
            console.error("❌ No 24-hour average data available.");
            return;
        }

        // ✅ ตรวจสอบค่า และปรับทศนิยมเป็น 2 ตำแหน่ง
        const temperature = data.temperature !== "N/A" && data.temperature !== null ? `${parseFloat(data.temperature).toFixed(2)}°C` : "N/A°C";
        const humidity = data.humidity !== "N/A" && data.humidity !== null ? `${parseFloat(data.humidity).toFixed(2)}%` : "N/A%";
        const pm2_5 = data.pm2_5 !== "N/A" && data.pm2_5 !== null ? parseFloat(data.pm2_5).toFixed(2) : "N/A";
        const pm0_1 = data.pm0_1_predicted !== "N/A" && data.pm0_1_predicted !== null ? parseFloat(data.pm0_1_predicted).toFixed(2) : "N/A";

   
        document.getElementById("pm25_24h").innerText = `${pm2_5} mg/m³`;
        document.getElementById("pm01_24h").innerText = `${pm0_1} mg/m³`;
        document.getElementById("temperature_24h").innerText = `${temperature}`;
        document.getElementById("humidity_24h").innerText = `${humidity}`; 

        // ✅ อัปเดตสถานะ PM2.5
        if (pm2_5 !== "N/A") {
            const { status, icon } = getPM25Status(parseFloat(pm2_5));
            document.getElementById("status_pm25_text_24h").innerText = status;
            document.getElementById("status_pm25_icon_24h").src = icon;
        }

        // ✅ อัปเดตสถานะ PM0.1
        if (pm0_1 !== "N/A") {
            const { status, icon } = getPM01Status(parseFloat(pm0_1));
            document.getElementById("status_pm01_text_24h").innerText = status;
            document.getElementById("status_pm01_icon_24h").src = icon;
        }

    } catch (error) {
        console.error("❌ Error fetching 24-hour data: ", error);
    }
}



// =============================================
// ฟังก์ชันกำหนดระดับ PM2.5
// =============================================
function getPM25Status(pm25) {
    if (pm25 <= 9.0) {
        return { status: "ดี", icon: "IMG/Status/normal.png" };
    } else if (pm25 <= 35.4) {
        return { status: "เฝ้าระวัง", icon: "IMG/Status/alert.png" };
    } else {
        return { status: "อันตราย", icon: "IMG/Status/warning.png" };
    }
}
// =============================================
// ฟังก์ชันอัพเดทการ์ด 
// =============================================
function updateAirQualityUI(pm25) {
    let backgroundElement = document.querySelector(".background-img"); // ดึง class background-img
    let iconElement = document.getElementById("status_icon_sec");
    let textElement = document.getElementById("status_text_sec");
    let descriptionElement = document.querySelector(".description"); // ดึงข้อความ description

    if (!backgroundElement || !iconElement || !textElement || !descriptionElement) {
        console.warn("⚠️ ไม่พบ element สำหรับอัปเดต UI");
        return;
    }

    let statusInfo = getPM25Status(pm25);

    if (statusInfo.status === "ดี") {
        backgroundElement.style.background = "url('IMG/BG-status/BG-G.png.webp') no-repeat center";
        backgroundElement.style.backgroundSize = "cover";
        iconElement.src = "IMG/icon-face/Icon-good.png";
        textElement.innerText = "เหมาะสม";
        descriptionElement.innerHTML = "คุณภาพอากาศอยู่ในเกณฑ์ที่เหมาะสม<br>ทุกคนสามารถทำกิจกรรมต่าง ๆ ได้ตามปกติ";
    } else if (statusInfo.status === "เฝ้าระวัง") {
        backgroundElement.style.background = "url('IMG/BG-status/BG-W.png') no-repeat center";
        backgroundElement.style.backgroundSize = "cover";
        iconElement.src = "IMG/icon-face/Icon-normal.png";
        textElement.innerText = "เฝ้าระวัง";
        descriptionElement.innerHTML = "คุณภาพอากาศอยู่ในเกณฑ์ที่อันตราย<br>ควรหลีกเลี่ยงสถานที่นี้หรือควรปรับ<br>คุณภาพอากาศให้เหมาะสม";
    } else {
        backgroundElement.style.background = "url('IMG/BG-status/BG-D.png') no-repeat center";
        backgroundElement.style.backgroundSize = "cover";
        iconElement.src = "IMG/icon-face/Icon-dangerous.png";
        textElement.innerText = "อันตราย";
        descriptionElement.innerHTML = "คุณภาพอากาศอยู่ในเกณฑ์ที่อันตราย<br>ควรหลีกเลี่ยงสถานที่นี้เพื่อความปลอดภัย";
    }
}



// =========================================
// อัปเดต UI สำหรับ PM2.5
// =========================================
function updatePM25UI(cardId, pm25Value) {
    const { status, icon } = getPM25Status(pm25Value);

    let statusTextElement = document.querySelector(`#${cardId} #status_pm25_text_now`);
    let statusIconElement = document.querySelector(`#${cardId} #status_pm25_now`);

    if (statusTextElement) {
        statusTextElement.innerText = status;
    } else {
        console.warn(`⚠️ ไม่พบ element: #${cardId} #status_pm25_text_now (อาจถูกลบไปแล้ว)`);
    }

    if (statusIconElement) {
        statusIconElement.src = icon;
    } else {
        console.warn(`⚠️ ไม่พบ element: #${cardId} #status_pm25_now (อาจถูกลบไปแล้ว)`);
    }
}

// =========================================
//  ดึงข้อมูล API และอัปเดต PM2.5
// =========================================

async function fetchAndUpdatePM25() {
    try {
        const response = await fetch('http://127.0.0.1:8000/average_pm_data_1m');
        const data = await response.json();

        if (!data || data.error) {
            console.error("❌ No data received from API.");
            return;
        }

        const pm25 = parseFloat(data.pm2_5);

        // อัปเดต UI สำหรับแต่ละช่วงเวลา
        updatePM25UI("card-1h", pm25);
        updatePM25UI("card-24h", pm25);

    } catch (error) {
        console.error("❌ Error fetching PM2.5 data: ", error);
    }
}

// =============================================
// ฟังก์ชันกำหนดระดับ PM0.1
// =============================================
function getPM01Status(pm01) {
    if (pm01 <= 0.12) {
        return { status: "ดี", icon: "IMG/Status/normal.png" };
    } else if (pm01 <= 0.94) {
        return { status: "เฝ้าระวัง", icon: "IMG/Status/alert.png" };
    } else {
        return { status: "อันตราย", icon: "IMG/Status/warning.png" };
    }
}

// =============================================
// ฟังก์ชันอัปเดต UI สำหรับ PM0.1
// =============================================
function updatePM01UI(cardId, pm01Value) {
    const { status, icon } = getPM01Status(pm01Value);

    let statusTextElement = document.querySelector(`#${cardId} #status_pm01_text_now`);
    let statusIconElement = document.querySelector(`#${cardId} #status_pm01_now`);

    if (statusTextElement) {
        statusTextElement.innerText = status;
    } else {
        console.warn(`⚠️ ไม่พบ element: #${cardId} #status_pm01_text_now (อาจถูกลบไปแล้ว)`);
    }

    if (statusIconElement) {
        statusIconElement.src = icon;
    } else {
        console.warn(`⚠️ ไม่พบ element: #${cardId} #status_pm01_now (อาจถูกลบไปแล้ว)`);
    }
}

// =============================================
//  ฟังก์ชันดึงข้อมูล PM0.1 และอัปเดตค่าบน UI
// =============================================
async function fetchAndUpdatePM01() {
    try {
        const response = await fetch('http://127.0.0.1:8000/average_pm_data_1m');
        const data = await response.json();

        if (!data || data.error) {
            console.error("❌ No data received from API.");
            return;
        }

        const pm01 = parseFloat(data.pm0_1_predicted);

        // อัปเดต UI สำหรับแต่ละช่วงเวลา
        updatePM01UI("card-1h", pm01);
        updatePM01UI("card-24h", pm01);

    } catch (error) {
        console.error("❌ Error fetching PM0.1 data: ", error);
    }
}


let simulatedData = []; 
let currentIndex = 0;
let lastDataTimestamp = null; 

// =============================================
//  ฟังก์ชันสุ่มค่า Normal Distribution
// =============================================

function generateRandomNormal(mean, sd) {
    if (isNaN(mean) || isNaN(sd) || sd <= 0) {
        console.warn(`⚠️ ค่า Mean (${mean}) หรือ SD (${sd}) ผิดปกติ, ใช้ค่า Mean แทน`);
        return mean;
    }
    let u1 = Math.random();
    let u2 = Math.random();
    let z = Math.sqrt(-2.0 * Math.log(u1)) * Math.cos(2.0 * Math.PI * u2);
    let result = mean + z * sd;
    
    console.log(`🎲 Randomized: mean=${mean}, sd=${sd}, result=${result.toFixed(2)}`);
    return result;
}

// =============================================
//  ฟังก์ชันสร้างค่าจำลอง 60 วินาที
// =============================================าที
function generateSimulatedSecData(meanValues, sdValues) {
    console.log("🚀 Generating new simulated data...");
    simulatedData = Array.from({ length: 60 }, () => ({
        pm25_sec: generateRandomNormal(meanValues.pm25_sec, sdValues.pm25_sec),
        pm01_sec: generateRandomNormal(meanValues.pm01_sec, sdValues.pm01_sec),
        temperature_sec: generateRandomNormal(meanValues.temperature_sec, sdValues.temperature_sec),
        humidity_sec: generateRandomNormal(meanValues.humidity_sec, sdValues.humidity_sec),
    }));
    currentIndex = 0;

    console.log("📊 Simulated data (First 5):", simulatedData.slice(0, 5));
}

// =============================================
//  อัปเดตค่าบน UI ทุกวินาที
// =============================================
function updateLiveSecData() {
    if (currentIndex < simulatedData.length) {
        let pm25 = parseFloat(simulatedData[currentIndex].pm25_sec).toFixed(2);
        let pm01 = parseFloat(simulatedData[currentIndex].pm01_sec).toFixed(2);
        let temp = parseFloat(simulatedData[currentIndex].temperature_sec).toFixed(2);
        let humidity = parseFloat(simulatedData[currentIndex].humidity_sec).toFixed(2);

        console.log(`📡 Updating UI [${currentIndex + 1}/60]:`, { pm25, pm01, temp, humidity });

        // ✅ อัปเดตค่าบน UI
        document.getElementById("pm25_sec").innerText = `${pm25} mg/m³`;
        document.getElementById("pm01_sec").innerText = `${pm01} mg/m³`;
        document.getElementById("temperature_sec").innerText = `${temp}°C`;
        document.getElementById("humidity_sec").innerText = `${humidity}%`; 

        // ✅ อัปเดตสถานะ PM2.5 โดยใช้ฟังก์ชันเดิม
        const { status, icon } = getPM25Status(parseFloat(pm25));
        document.getElementById("status_pm25_text_sec").innerText = status;
        document.getElementById("status_pm25_sec").src = icon;


        // ✅ อัปเดตสถานะ PM0.1 โดยใช้ฟังก์ชัน getPM01Status
        const { status: pm01Status, icon: pm01Icon } = getPM01Status(parseFloat(pm01));

        document.getElementById("status_pm01_text_sec").innerText = pm01Status;
        document.getElementById("status_pm01_sec").src = pm01Icon;


        // ✅ อัปเดตพื้นหลังและไอคอนตามค่าฝุ่น PM2.5
        updateAirQualityUI(parseFloat(pm25));

        currentIndex++;
    } else {
        console.warn("🔄 รีเซ็ตข้อมูลสุ่มใหม่");
        currentIndex = 0;
    }
}

// =============================================
//  ดึงค่าจาก API (ค่าจริงทุก 1 นาที)
// =============================================
async function fetchSecData() {
    try {
        console.log("🔄 Fetching latest sec data...");

        const response = await fetch('http://127.0.0.1:8000/average_pm_data_1m');
        const data = await response.json();

        console.log("📥 Data received:", data);

        if (!data || data.error) {
            console.error("❌ No data received from API.");
            return;
        }

        // 🔹 ตรวจสอบ timestamp ของข้อมูลล่าสุด
        const newTimestamp = data.timestamp || Date.now(); // ถ้า API ไม่มี timestamp ให้ใช้เวลาปัจจุบัน
        if (newTimestamp === lastDataTimestamp) {
            console.log("🔄 No new data. Using previous simulation.");
            return; // ถ้าไม่มีข้อมูลใหม่ ไม่ต้องสุ่มค่าใหม่
        }
        lastDataTimestamp = newTimestamp; // อัปเดต timestamp ล่าสุด

        // 🔹 ดึงค่า Mean จาก API
        const meanValues = {
            pm25_sec: parseFloat(data.pm2_5) || 0,
            pm01_sec: parseFloat(data.pm0_1_predicted) || 0,
            temperature_sec: parseFloat(data.temperature) || 0,
            humidity_sec: parseFloat(data.humidity) || 0,
        };

        console.log("📊 Mean values:", meanValues);

        // 🔹 ดึงค่า SD จาก API
        const sdResponse = await fetch('http://127.0.0.1:8000/sd_pm_data_1m');
        const sdData = await sdResponse.json();

        console.log("📥 SD Data received:", sdData);

        if (!sdData || sdData.error) {
            console.error("❌ No SD data received.");
            return;
        }

        const sdValues = {
            pm25_sec: parseFloat(sdData.PM25_SD) || 0.1,
            pm01_sec: parseFloat(sdData.PM01_SD) || 0.01,
            temperature_sec: parseFloat(sdData.Temperature_SD) || 0.1,
            humidity_sec: parseFloat(sdData.Humidity_SD) || 0.1,
        };

        console.log("📊 SD values:", sdValues);

        // 🔹 สร้างค่าจำลอง 60 วินาที
        generateSimulatedSecData(meanValues, sdValues);

    } catch (error) {
        console.error("❌ Error fetching latest data: ", error);
    }
}


// =============================================
// เริ่มต้นการทำงาน
// =============================================

window.onload = function() {
    fetch1hData();
    fetch24hData();
    fetchSecData();
    fetchAndUpdatePM25();
    fetchAndUpdatePM01(); // ✅ เพิ่มการดึงข้อมูล PM0.1

    setInterval(() => {
        fetchAndUpdatePM25();
        fetchAndUpdatePM01(); // ✅ อัปเดตค่าทุกวินาที
        updateLiveSecData();
        fetchSecData();
    }, 1000);

  
    setInterval(() => {
        fetch1hData();    
    }, 30000);

    setInterval(() => {
        fetch24hData();    
    }, 60000);

};

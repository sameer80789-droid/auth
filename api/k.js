export default function handler(req, res) {
  res.setHeader('Content-Type', 'application/json');
  
  // Get the key parameter sent by the app
  const key = req.query.key || req.body?.key;

  // Define your valid keys (or connect this to a database / environment variable)
  const validKeys = ["KEY-12345", "ANDROID-VIP-2026", "SAMEER-TEST-KEY"];

  if (key && validKeys.includes(key)) {
    return res.status(200).json({
      success: true,
      message: "Key validated successfully",
      status: "active"
    });
  } else {
    return res.status(401).json({
      success: false,
      message: "Invalid or missing license key"
    });
  }
}
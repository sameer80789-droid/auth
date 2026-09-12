export default function handler(req, res) {
  res.setHeader('Content-Type', 'application/json');
  res.status(200).json({
    success: true,
    message: "Authenticated successfully",
    // Match the JSON keys expected by your app's native library
  });
}
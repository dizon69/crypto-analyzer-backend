const { getTopDepthStatus } = require("../collector/depth_ws");

function getDepthData(req, reply) {
  try {
    const data = getTopDepthStatus(10); // ambil top 10 coin
    return reply.send({
      success: true,
      data
    });
  } catch (err) {
    return reply.code(500).send({
      success: false,
      message: "Failed to retrieve depth data",
      error: err.message
    });
  }
}

module.exports = {
  getDepthData
};

using Microsoft.AspNetCore.Mvc;
using System.Text;
using System.Text.Json;

namespace ApiGateway.Controllers;

[ApiController]
[Route("api/[controller]")]
public class InferenceController : ControllerBase
{
    private readonly IHttpClientFactory _httpClientFactory;
    private readonly ILogger<InferenceController> _logger;

    public InferenceController(IHttpClientFactory httpClientFactory, ILogger<InferenceController> logger)
    {
        _httpClientFactory = httpClientFactory;
        _logger = logger;
    }

    /// <summary>
    /// Proxies the inference request to the AI Service.
    /// This pattern abstracts the backend AI service details from the client.
    /// </summary>
    /// <param name="request">The prediction request payload.</param>
    /// <returns>The prediction result.</returns>
    [HttpPost]
    public async Task<IActionResult> Predict([FromBody] JsonElement request)
    {
        try
        {
            _logger.LogInformation("Received inference request via Gateway.");

            // Create client named "AIService" (configured in Program.cs with Polly policies)
            var client = _httpClientFactory.CreateClient("AIService");

            var jsonContent = new StringContent(
                request.ToString(),
                Encoding.UTF8,
                "application/json");

            // Forward request to AI Service
            var response = await client.PostAsync("/predict", jsonContent);

            if (response.IsSuccessStatusCode)
            {
                var content = await response.Content.ReadAsStringAsync();
                _logger.LogInformation("AI Service responded successfully.");
                return Ok(JsonSerializer.Deserialize<JsonElement>(content));
            }
            else
            {
                _logger.LogWarning($"AI Service returned an error: {response.StatusCode}");
                return StatusCode((int)response.StatusCode, "Error connecting to AI Service");
            }
        }
        catch (Exception ex)
        {
            _logger.LogError($"Gateway Error: {ex.Message}");
            return StatusCode(500, "Internal Gateway Error");
        }
    }

    [HttpGet("health")]
    public IActionResult Health()
    {
        return Ok(new { status = "Gateway Healthy", timestamp = DateTime.UtcNow });
    }
}

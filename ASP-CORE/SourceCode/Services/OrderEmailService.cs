using System.Net;
using System.Net.Mail;
using System.Text;
using SourceCode.Models;

namespace SourceCode.Services;

public class OrderEmailService(IConfiguration config, ILogger<OrderEmailService> logger)
{
    public async Task SendAsync(Order order)
    {
        var address = config["Email:Address"];
        var password = config["Email:AppPassword"];
        if (string.IsNullOrWhiteSpace(address) || string.IsNullOrWhiteSpace(password))
        {
            logger.LogWarning("Email is not configured. Order {OrderId} was saved.", order.Id);
            return;
        }
        try
        {
            using var message = new MailMessage(address, order.Email)
            {
                Subject = $"CineNghia - xác nhận đơn #{order.Id}",
                BodyEncoding = Encoding.UTF8,
                SubjectEncoding = Encoding.UTF8,
                IsBodyHtml = true
            };
            var lines = string.Join("", order.Items.Select(x =>
                $"<li>{WebUtility.HtmlEncode(x.Movie?.Title)} × {x.Quantity}: {(x.UnitPrice * x.Quantity):N0}đ</li>"));
            message.Body = $"<h2>Đơn hàng #{order.Id}</h2><ul>{lines}</ul>" +
                $"<p>Tổng tiền: {order.Total:N0}đ</p><p>Giao đến: {WebUtility.HtmlEncode(order.CustomerName)}, {WebUtility.HtmlEncode(order.Address)}</p>";
            using var client = new SmtpClient("smtp.gmail.com", 587)
            {
                EnableSsl = true,
                Credentials = new NetworkCredential(address, password)
            };
            await client.SendMailAsync(message);
        }
        catch (Exception ex)
        {
            logger.LogWarning(ex, "Order {OrderId} was saved but confirmation email failed.", order.Id);
        }
    }
}

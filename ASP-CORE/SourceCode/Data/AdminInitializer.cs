using Microsoft.AspNetCore.Identity;

namespace SourceCode.Data;

public static class AdminInitializer
{
    public static async Task EnsureAdminAsync(IServiceProvider services, string email, string password)
    {
        var users = services.GetRequiredService<UserManager<IdentityUser>>();
        if (await users.FindByEmailAsync(email) is not null) return;
        var result = await users.CreateAsync(new IdentityUser
        {
            UserName = email,
            Email = email,
            EmailConfirmed = true
        }, password);
        if (!result.Succeeded)
            throw new InvalidOperationException("Could not create admin account: " +
                string.Join("; ", result.Errors.Select(x => x.Description)));
    }
}

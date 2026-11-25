using Microsoft.AspNetCore.Identity;
using Microsoft.EntityFrameworkCore;
using SourceCode.Data;

var builder = WebApplication.CreateBuilder(args);

// Add services to the container.
var connectionString = builder.Configuration.GetConnectionString("DefaultConnection") ?? throw new InvalidOperationException("Connection string 'DefaultConnection' not found.");
builder.Services.AddDbContext<ApplicationDbContext>(options =>
    options.UseSqlServer(connectionString));
builder.Services.AddDatabaseDeveloperPageExceptionFilter();

builder.Services.AddDefaultIdentity<IdentityUser>(options => options.SignIn.RequireConfirmedAccount = true)
    .AddEntityFrameworkStores<ApplicationDbContext>();
var adminEmail = builder.Configuration["Admin:Email"] ?? throw new InvalidOperationException("Admin:Email is missing.");
builder.Services.AddAuthorizationBuilder().AddPolicy("AdminOnly", policy =>
    policy.RequireAssertion(context => string.Equals(context.User.Identity?.Name, adminEmail, StringComparison.OrdinalIgnoreCase)));
builder.Services.AddControllersWithViews();
builder.Services.AddDistributedMemoryCache();
builder.Services.AddHttpContextAccessor();
builder.Services.AddSession(options =>
{
    options.IdleTimeout = TimeSpan.FromMinutes(100);
    options.Cookie.HttpOnly = true;
    options.Cookie.IsEssential = true;
});
builder.Services.AddScoped<SourceCode.Services.CartService>();
builder.Services.AddTransient<SourceCode.Services.OrderEmailService>();

var app = builder.Build();

// Configure the HTTP request pipeline.
if (app.Environment.IsDevelopment())
{
    app.UseMigrationsEndPoint();
}
else
{
    app.UseExceptionHandler("/Home/Error");
    // The default HSTS value is 30 days. You may want to change this for production scenarios, see https://aka.ms/aspnetcore-hsts.
    app.UseHsts();
}

app.UseHttpsRedirection();
// Runtime uploads are not part of the build-time MapStaticAssets manifest.
app.UseStaticFiles();
app.UseRouting();

app.UseAuthentication();
app.UseAuthorization();
app.UseSession();

app.MapStaticAssets();

app.MapControllerRoute(
    name: "default",
    pattern: "{controller=Movies}/{action=Index}/{id?}")
    .WithStaticAssets();

app.MapRazorPages()
   .WithStaticAssets();

using (var scope = app.Services.CreateScope())
{
    var db = scope.ServiceProvider.GetRequiredService<ApplicationDbContext>();
    await db.Database.MigrateAsync();
    await DbInitializer.SeedAsync(db);
    if (!app.Environment.IsDevelopment())
    {
        var adminPassword = app.Configuration["Admin:Password"];
        if (string.IsNullOrWhiteSpace(adminPassword))
            throw new InvalidOperationException("Admin:Password must be configured for production.");
        await AdminInitializer.EnsureAdminAsync(scope.ServiceProvider, adminEmail, adminPassword);
    }
}

app.Run();

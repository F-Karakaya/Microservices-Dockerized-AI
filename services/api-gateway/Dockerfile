# Dockerfile for ASP.NET Core API Gateway
# Uses multi-stage build to separate build environment from runtime environment.

# Stage 1: Build
FROM mcr.microsoft.com/dotnet/sdk:8.0 AS build
WORKDIR /src

# Copy csproj and restore as distinct layers
COPY ["api-gateway.csproj", "./"]
RUN dotnet restore "api-gateway.csproj"

# Copy everything else and build
COPY . .
RUN dotnet publish "api-gateway.csproj" -c Release -o /app/publish /p:UseAppHost=false

# Stage 2: Runtime
# Uses the lighter ASP.NET Core runtime image
FROM mcr.microsoft.com/dotnet/aspnet:8.0 AS final
WORKDIR /app
EXPOSE 8080
EXPOSE 8081

# Copy build artifacts from previous stage
COPY --from=build /app/publish .

# Set entry point
ENTRYPOINT ["dotnet", "api-gateway.dll"]

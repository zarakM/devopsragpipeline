# ASP.NET Core Order Service Dockerfile
FROM mcr.microsoft.com/dotnet/sdk:8.0 AS build
WORKDIR /src

# Copy csproj and restore as distinct layers
COPY ["Orders.Service/Orders.Service.csproj", "Orders.Service/"]
RUN dotnet restore "Orders.Service/Orders.Service.csproj"

# Copy everything else and build
COPY . .
WORKDIR "/src/Orders.Service"
RUN dotnet build "Orders.Service.csproj" -c Release -o /app/build

FROM build AS publish
RUN dotnet publish "Orders.Service.csproj" -c Release -o /app/publish /p:UseAppHost=false

FROM mcr.microsoft.com/dotnet/aspnet:8.0 AS final
WORKDIR /app
EXPOSE 80
EXPOSE 443
COPY --from=publish /app/publish .
ENTRYPOINT ["dotnet", "Orders.Service.dll"]

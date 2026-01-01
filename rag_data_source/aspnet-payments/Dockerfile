# ASP.NET Core Payment Service Dockerfile
FROM mcr.microsoft.com/dotnet/sdk:6.0 AS build
WORKDIR /src

COPY ["Payments.Service/Payments.Service.csproj", "Payments.Service/"]
RUN dotnet restore "Payments.Service/Payments.Service.csproj"

COPY . .
WORKDIR "/src/Payments.Service"
RUN dotnet build "Payments.Service.csproj" -c Release -o /app/build

FROM build AS publish
RUN dotnet publish "Payments.Service.csproj" -c Release -o /app/publish

FROM mcr.microsoft.com/dotnet/aspnet:6.0 AS final
WORKDIR /app
EXPOSE 80
COPY --from=publish /app/publish .
ENTRYPOINT ["dotnet", "Payments.Service.dll"]

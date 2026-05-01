from src.ft_parser import MapParser

parser = MapParser()
try:
    print("lparsing ya wld 3mi\n")
    parsed = parser.file_parsing("./test.txt")

    print("\n✅ PARSING! this is the ParsedMap:")
    print(f"🚁 Drones: {parsed.nb_drones}")
    print(f"🟢 Start: {parsed.start_hub.name} (Color: {parsed.start_hub.color})")
    print(f"🔴 End: {parsed.end_hub.name} (Color: {parsed.end_hub.color})")

    print("🏢 Hubs (3adyin):")
    for name, zone in parsed.zones.items():
        if name not in (parsed.start_hub.name, parsed.end_hub.name):
            print(f"   * {name} | Type: {zone.zone_type.value} | Max Drones: {zone.max_drones} | color: {zone.color}")

    print("🛣️ Connections:")
    for conn in parsed.connections:
        print(f"   * {conn.zone1.name} <-> {conn.zone2.name} | Max Capacity: {conn.max_link_capacity}")

except Exception as e:
    print(f"\n❌ ERROR: {e}")
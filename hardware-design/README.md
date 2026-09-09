# hardware-design

CAD files, PCB schematics, and mechanical models for the smart bin enclosure.

From the pitch deck's mechanical drawing, the bin has:
- Lid + waste input chute (top)
- Equal-analyze / first-level segregation chamber
- Shaking mechanism (MG996R servo)
- Rotary segregation unit with Y-junction diverter
- Separate bio bin and non-bio bin compartments
- Hazardous waste tray (bottom, likely removable for safe disposal)

Bill of materials totals ~₹2,800 (sensors ₹400, components ₹400, electrical ₹800, hardware ₹600
per the cost breakdown slide — cross-check against `docs/` if these move).

Drop CAD source files (Fusion 360 / SolidWorks / FreeCAD) here. Keep exported renders out of git
(see root `.gitignore`) — link to a shared drive for those instead if the team needs to browse
them without opening CAD software.

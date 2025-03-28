local HttpService = game:GetService("HttpService")
local partFolder = workspace:WaitForChild("PartFolder") -- Folder containing the parts
local serverUrl = "" -- Insert your server URL here (Remember to put, "/screen" after main link for it to work correctly)
local updateInterval = 1 -- Time in seconds between updates
local numCols = 0 -- Add your col numbers
local numRows = 0 -- Add your row numbers

-- Function to sort parts based on their position
local function sortParts(parts)
	table.sort(parts, function(a, b)
		if a.Position.Y == b.Position.Y then
			return a.Position.X < b.Position.X
		else
			return a.Position.Y > b.Position.Y
		end
	end)
	return parts
end

-- Store parts
local parts = partFolder:GetChildren()
parts = sortParts(parts)

local function updateParts(changes, colors)
	for i, changeIndex in ipairs(changes) do
		local part = parts[changeIndex + 1]
		local color = colors[i]
		part.Color = Color3.fromRGB(color[1], color[2], color[3])
	end
end

local function fetchData()
	local success, response = pcall(function()
		return HttpService:GetAsync(serverUrl)
	end)

	if success then
		local colorData
		local parseSuccess, parseError = pcall(function()
			colorData = HttpService:JSONDecode(response)
		end)

		if parseSuccess then
			local changes = colorData["changes"]
			local colors = colorData["colors"]

			if #changes == #colors then
				updateParts(changes, colors)
			else
				warn("Mismatch in changes and colors lengths")
			end
		else
			warn("Failed to parse JSON: " .. parseError)
		end
	else
		warn("Failed to fetch data: " .. response)
	end
end

while true do
	fetchData()
	wait(updateInterval)
end

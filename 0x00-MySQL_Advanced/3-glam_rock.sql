-- A sql script that lists out bands based on their logevity
SELECT `band_name`, COALESCE(`split`, 2022) - `formed` AS lifespan FROM metal_bands 
WHERE `style` like '%Glam rock%' 
ORDER BY lifespan DESC;

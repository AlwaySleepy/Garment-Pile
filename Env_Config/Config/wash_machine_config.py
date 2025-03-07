import os


class Config:
    def __init__(self):
        self.path = os.getcwd()

        # ------------Franka Robot Config------------ #
        self.robot_position = [-0.68, -0.05, 0.11]  # sequence:"XYZ"

        # sequence:"XYZ", input degrees, e.g.[0.0, 0.0, 90.0]
        self.robot_orientation = [0.0, 0.0, 0.0]

        # franka move positions sequence
        self.target_positions = [
            [-0.15, -0.05, 0.55],  # Enter Wash Machine
            [-0.8, -0.05, 0.85],  # Retrieve out the garment from Wash Machine
            [-1.2, -0.55, 1.1],  # Move to the basket
        ]

        # ------------Wash_Machine Config------------ #
        self.wm_position = [-0.05, 0.0, 0.58]  # sequence:"XYZ"

        # sequence:"XYZ", input degrees, e.g.[0.0, 0.0, 90.0]
        self.wm_orientation = [0.0, 0.0, 0.0]

        self.wm_scale = [0.8, 0.8, 0.8]  # sequence:"XYZ", e.g.[1.0, 1.0, 1.0]

        self.wm_prim_path = "/World/Wash_Machine"

        # Washing_Machine_Usd_Path(no need to change)
        self.wm_usd_path = self.path + "/Assets/Wash_Machine/wash_machine.usd"

        # ------------Room Config------------ #
        # Room_Usd_Path(no need to change)
        self.room_usd_path = self.path + "/Assets/Scene/wash_machine_scene/scene.usd"

        self.room_position = [-3.39737, -1.65851, 0.0]  # sequence:"XYZ"

        self.room_orientation = [
            0.0,
            0.0,
            0.0,
        ]  # sequence:"XYZ", input degrees, e.g.[0.0, 0.0, 90.0]

        self.room_scale = [0.013, 0.013, 0.012]  # sequence:"XYZ", e.g.[1.0, 1.0, 1.0]

        self.room_prim_path = "/World/Room"

        # ------------Basket Config------------ #
        # Basket_Usd_Path(no need to change)
        self.basket_usd_path = self.path + "/Assets/Basket/basket.usd"

        self.basket_position = [-1.08, -0.5, 0.1682]  # sequence:"XYZ"

        self.basket_orientation = [
            0.0,
            0.0,
            90.0,
        ]  # sequence:"XYZ", input degrees, e.g.[0.0, 0.0, 90.0]

        self.basket_scale = [0.45, 0.45, 0.45]  # sequence:"XYZ", e.g.[1.0, 1.0, 1.0]

        self.basket_prim_path = "/World/Basket"

        # ------------Base Config------------ #
        # Base_Layer_Usd_Path(no need to change)
        self.base_usd_path = self.path + "/Assets/Robot_Base/base_layer_no_physics.usd"

        self.base_position = [-0.79863, -0.05867, -0.01252]  # sequence:"XYZ"

        self.base_orientation = [
            0.0,
            0.0,
            0.0,
        ]  # sequence:"XYZ", input degrees, e.g.[0.0, 0.0, 90.0]

        self.base_scale = [0.5, 0.5, 0.45]  # sequence:"XYZ", e.g.[1.0, 1.0, 1.0]

        self.base_prim_path = "/World/Base"

        # ------------Point_Cloud Camera Config------------ #
        self.point_cloud_camera_position = [-1.70461, 0, 1.225]

        self.point_cloud_camera_orientation = [0, 22, 0]

        # ------------Recording Camera Config------------ #
        self.recording_camera_position = [-4.17, -2.5, 2.2]

        self.recording_camera_orientation = [0, 22, 30]

        # ------------Garment Config------------ #
        # Please make sure the length of (position/orientation/scale) array
        # exactly match or more than the garment num.
        self.garment_num = 5

        self.garment_position = [
            [-2, -0.05, 0.95],
            [-3, -0.05, 0.95],
            [-4, -0.05, 0.95],
            [-5, -0.05, 0.95],
            [-6, -0.05, 0.95],
            [-7, -0.05, 0.95],
            [-8, -0.05, 0.95],
        ]

        self.garment_orientation = [
            [0.0, 0.0, -90.0],
            [0.0, 0.0, -90.0],
            [0.0, 0.0, -90.0],
            [0.0, 0.0, -90.0],
            [0.0, 0.0, -90.0],
            [0.0, 0.0, -90.0],
            [0.0, 0.0, -90.0],
        ]

        self.garment_scale = [
            [0.0065, 0.0065, 0.0065],
            [0.0065, 0.0065, 0.0065],
            [0.0065, 0.0065, 0.0065],
            [0.0065, 0.0065, 0.0065],
            [0.0065, 0.0065, 0.0065],
            [0.0065, 0.0065, 0.0065],
            [0.0065, 0.0065, 0.0065],
        ]

        # Garment_Usd_Path(no need to change)
        self.clothpath = {
            "cloth0": self.path
            + "/Assets/Garment/Dress/Long_NoSleeve/DLNS_Dress003_0/DLNS_Dress003_0_obj.usd",
            "cloth1": self.path
            + "/Assets/Garment/Scarf_Tie/ST_Scarf-001/ST_Scarf-001_obj.usd",
            "cloth2": self.path
            + "/Assets/Garment/Dress/Long_Gallus/DLG_Dress032_1/DLG_Dress032_1_obj.usd",
            "cloth3": self.path
            + "/Assets/Garment/Tops/Collar_Lsleeve_FrontClose/TCLC_002/TCLC_002_obj.usd",
            "cloth4": self.path
            + "/Assets/Garment/Tops/Collar_Lsleeve_FrontClose/TCLC_015/TCLC_015_obj.usd",
            "cloth5": self.path
            + "/Assets/Garment/Dress/Long_ShortSleeve/DLSS_Dress037_0/DLSS_Dress037_0_obj.usd",
            "cloth6": self.path
            + "/Assets/Garment/Dress/Short_LongSleeve/DSLS_dress271/DSLS_dress271_obj.usd",
            "cloth7": self.path
            + "/Assets/Garment/Skirt/Long/SL_skirt148/SL_skirt148_obj.usd",
            "cloth8": self.path
            + "/Assets/Garment/Skirt/Short/SL_Skirt017_1/SL_Skirt017_1_obj.usd",
            "cloth9": self.path
            + "/Assets/Garment/Scarf_Tie/ST_Tie026/ST_Tie026_obj.usd",
            # Dress-Long_Gallus
            "cloth10": self.path
            + "/Assets/Garment/Dress/Long_Gallus/DLG_Dress035_0/DLG_Dress035_0_obj.usd",
            "cloth11": self.path
            + "/Assets/Garment/Dress/Long_Gallus/DLG_Dress079/DLG_Dress079_obj.usd",
            "cloth12": self.path
            + "/Assets/Garment/Dress/Long_Gallus/DLG_Dress099/DLG_Dress099_obj.usd",
            "cloth13": self.path
            + "/Assets/Garment/Dress/Long_Gallus/DLG_Dress101/DLG_Dress101_obj.usd",
            "cloth14": self.path
            + "/Assets/Garment/Dress/Long_Gallus/DLG_Dress105/DLG_Dress105_obj.usd",
            "cloth15": self.path
            + "/Assets/Garment/Dress/Long_Gallus/DLG_Dress198/DLG_Dress198_obj.usd",
            "cloth16": self.path
            + "/Assets/Garment/Dress/Long_Gallus/DLG_Dress312/DLG_Dress312_obj.usd",
            "cloth17": self.path
            + "/Assets/Garment/Dress/Long_Gallus/DLG_Dress319/DLG_Dress319_obj.usd",
            "cloth18": self.path
            + "/Assets/Garment/Dress/Long_Gallus/DLG_Dress394/DLG_Dress394_obj.usd",
            "cloth19": self.path
            + "/Assets/Garment/Dress/Long_Gallus/DLG_Dress476/DLG_Dress476_obj.usd",
            "cloth20": self.path
            + "/Assets/Garment/Dress/Long_Gallus/DSNS_Dress123/DSNS_Dress123_obj.usd",
            # Dress-LongSleeve
            "cloth21": self.path
            + "/Assets/Garment/Dress/Long_LongSleeve/DLLS_Dress050_1/DLLS_Dress050_1_obj.usd",
            "cloth22": self.path
            + "/Assets/Garment/Dress/Long_LongSleeve/DLLS_dress230/DLLS_dress230_obj.usd",
            "cloth23": self.path
            + "/Assets/Garment/Dress/Long_LongSleeve/DLLS_Dress290/DLLS_Dress290_obj.usd",
            "cloth24": self.path
            + "/Assets/Garment/Dress/Long_LongSleeve/DLLS_Dress333/DLLS_Dress333_obj.usd",
            "cloth25": self.path
            + "/Assets/Garment/Dress/Long_LongSleeve/DLLS_Dress355/DLLS_Dress355_obj.usd",
            # Dress-LongNoSleeve
            "cloth26": self.path
            + "/Assets/Garment/Dress/Long_NoSleeve/DLNS_Dress003_1/DLNS_Dress003_1_obj.usd",
            "cloth27": self.path
            + "/Assets/Garment/Dress/Long_NoSleeve/DLNS_Dress010/DLNS_Dress010_obj.usd",
            "cloth28": self.path
            + "/Assets/Garment/Dress/Long_NoSleeve/DLNS_Dress011/DLNS_Dress011_obj.usd",
            "cloth29": self.path
            + "/Assets/Garment/Dress/Long_NoSleeve/DLNS_Dress021/DLNS_Dress021_obj.usd",
            "cloth30": self.path
            + "/Assets/Garment/Dress/Long_NoSleeve/DLNS_dress040/DLNS_dress040_obj.usd",
            "cloth31": self.path
            + "/Assets/Garment/Dress/Long_NoSleeve/DLNS_Dress131/DLNS_Dress131_obj.usd",
            "cloth32": self.path
            + "/Assets/Garment/Dress/Long_NoSleeve/DLNS_Dress240/DLNS_Dress240_obj.usd",
            "cloth33": self.path
            + "/Assets/Garment/Dress/Long_NoSleeve/DLNS_Dress291/DLNS_Dress291_obj.usd",
            "cloth34": self.path
            + "/Assets/Garment/Dress/Long_NoSleeve/DSNS_Dress049_1/DSNS_Dress049_1_obj.usd",
            "cloth35": self.path
            + "/Assets/Garment/Dress/Long_NoSleeve/DLNS_Dress030/DLNS_Dress030_obj.usd",
            # Dress-LongShortSleeve
            "cloth36": self.path
            + "/Assets/Garment/Dress/Long_ShortSleeve/DLSS_Dress051_1/DLSS_Dress051_1_obj.usd",
            "cloth37": self.path
            + "/Assets/Garment/Dress/Long_ShortSleeve/DLSS_Dress356/DLSS_Dress356_obj.usd",
            # Dress-LongTube
            "cloth38": self.path
            + "/Assets/Garment/Dress/Long_Tube/DLT_Dress036_0/DLT_Dress036_0_obj.usd",
            "cloth39": self.path
            + "/Assets/Garment/Dress/Long_Tube/DLT_Dress389/DLT_Dress389_obj.usd",
            # Dress-ShortGallus
            "cloth40": self.path
            + "/Assets/Garment/Dress/Short_Gallus/DSG_Dress102/DSG_Dress102_obj.usd",
            "cloth41": self.path
            + "/Assets/Garment/Dress/Short_Gallus/DSNS_Dress193/DSNS_Dress193_obj.usd",
            # one-piece
            "cloth42": self.path
            + "/Assets/Garment/One-piece/OP_Overall006/OP_Overall006_obj.usd",
            "cloth43": self.path
            + "/Assets/Garment/One-piece/OP_Overall015/OP_Overall015_obj.usd",
            "cloth44": self.path
            + "/Assets/Garment/One-piece/OP_overall033/OP_overall033_obj.usd",
            "cloth45": self.path
            + "/Assets/Garment/One-piece/OP_Overall055/OP_Overall055_obj.usd",
            "cloth46": self.path
            + "/Assets/Garment/One-piece/OP_Overall094/OP_Overall094_obj.usd",
            "cloth47": self.path
            + "/Assets/Garment/One-piece/OP_Overall123/OP_Overall123_obj.usd",
            # long-skirt
            "cloth48": self.path
            + "/Assets/Garment/Skirt/Long/SL_skirt023/SL_skirt023_obj.usd",
            "cloth49": self.path
            + "/Assets/Garment/Skirt/Long/SL_Skirt096/SL_Skirt096_obj.usd",
            "cloth50": self.path
            + "/Assets/Garment/Skirt/Long/SL_Skirt248/SL_Skirt248_obj.usd",
            "cloth51": self.path
            + "/Assets/Garment/Skirt/Long/SL_Skirt258/SL_Skirt258_obj.usd",
            "cloth52": self.path
            + "/Assets/Garment/Skirt/Long/SL_skirt293/SL_skirt293_obj.usd",
            "cloth53": self.path
            + "/Assets/Garment/Skirt/Long/SL_Skirt366/SL_Skirt366_obj.usd",
            # short-skirt
            "cloth54": self.path
            + "/Assets/Garment/Skirt/Short/SS_Skirt029/SS_Skirt029_obj.usd",
            "cloth55": self.path
            + "/Assets/Garment/Skirt/Short/SS_Skirt074/SS_Skirt074_obj.usd",
            "cloth56": self.path
            + "/Assets/Garment/Skirt/Short/SS_Skirt086/SS_Skirt086_obj.usd",
            "cloth57": self.path
            + "/Assets/Garment/Skirt/Short/SS_Skirt142/SS_Skirt142_obj.usd",
            "cloth58": self.path
            + "/Assets/Garment/Skirt/Short/SS_Skirt265/SS_Skirt265_obj.usd",
            "cloth59": self.path
            + "/Assets/Garment/Skirt/Short/SS_Skirt368/SS_Skirt368_obj.usd",
            # tops
            "cloth60": self.path
            + "/Assets/Garment/Tops/Collar_Lsleeve_FrontClose/TCLC_014/TCLC_014_obj.usd",
            "cloth61": self.path
            + "/Assets/Garment/Tops/Collar_Lsleeve_FrontClose/TCLC_Top566/TCLC_Top566_obj.usd",
            "cloth62": self.path
            + "/Assets/Garment/Tops/Collar_Lsleeve_FrontOpen/TCLO_048/TCLO_048_obj.usd",
            "cloth63": self.path
            + "/Assets/Garment/Tops/Collar_Lsleeve_FrontOpen/TCLO_Jacket134/TCLO_Jacket134_obj.usd",
            "cloth64": self.path
            + "/Assets/Garment/Tops/Collar_Lsleeve_FrontOpen/TCLO_Normal_Model_057/TCLO_Normal_Model_057_obj.usd",
            "cloth65": self.path
            + "/Assets/Garment/Tops/Collar_noSleeve_FrontClose/TCNC_model2_033/TCNC_model2_033_obj.usd",
            "cloth66": self.path
            + "/Assets/Garment/Tops/Collar_noSleeve_FrontClose/TCNC_Top086/TCNC_Top086_obj.usd",
            "cloth67": self.path
            + "/Assets/Garment/Tops/Collar_Ssleeve_FrontClose/TCSC_Jacket167/TCSC_Jacket167_obj.usd",
            "cloth68": self.path
            + "/Assets/Garment/Tops/Collar_Ssleeve_FrontClose/TCSC_polo004/TCSC_polo004_obj.usd",
            "cloth69": self.path
            + "/Assets/Garment/Tops/NoCollar_Lsleeve_FrontClose/TNLC_010/TNLC_010_obj.usd",
            "cloth70": self.path
            + "/Assets/Garment/Tops/NoCollar_Lsleeve_FrontClose/TNLC_Jumper002/TNLC_Jumper002_obj.usd",
            "cloth71": self.path
            + "/Assets/Garment/Tops/NoCollar_Lsleeve_FrontClose/TNLC_top189/TNLC_top189_obj.usd",
            "cloth72": self.path
            + "/Assets/Garment/Tops/NoCollar_Lsleeve_FrontClose/TNLC_Top400/TNLC_Top400_obj.usd",
            "cloth73": self.path
            + "/Assets/Garment/Tops/NoCollar_Lsleeve_FrontClose/TNLC_Top425/TNLC_Top425_obj.usd",
            "cloth74": self.path
            + "/Assets/Garment/Tops/NoCollar_Lsleeve_FrontClose/TNLC_Top504/TNLC_Top504_obj.usd",
            "cloth75": self.path
            + "/Assets/Garment/Tops/NoCollar_Lsleeve_FrontClose/TNLC_Top550/TNLC_Top550_obj.usd",
            "cloth76": self.path
            + "/Assets/Garment/Tops/NoCollar_Ssleeve_FrontClose/TNSC_Top626/TNSC_Top626_obj.usd",
            "cloth77": self.path
            + "/Assets/Garment/Tops/NoCollar_Ssleeve_FrontOpen/TNSO_model2_052/TNSO_model2_052_obj.usd",
            # trousers
            "cloth78": self.path
            + "/Assets/Garment/Trousers/Long/PL_030/PL_030_obj.usd",
            "cloth79": self.path
            + "/Assets/Garment/Trousers/Long/PL_047/PL_047_obj.usd",
            "cloth80": self.path
            + "/Assets/Garment/Trousers/Long/PL_071/PL_071_obj.usd",
            "cloth81": self.path
            + "/Assets/Garment/Trousers/Long/PL_LongPants003/PL_LongPants003_obj.usd",
            "cloth82": self.path
            + "/Assets/Garment/Trousers/Long/PL_M1_005/PL_M1_005_obj.usd",
            "cloth83": self.path
            + "/Assets/Garment/Trousers/Long/PL_M1_024/PL_M1_024_obj.usd",
            "cloth84": self.path
            + "/Assets/Garment/Trousers/Long/PL_M1_056/PL_M1_056_obj.usd",
            "cloth85": self.path
            + "/Assets/Garment/Trousers/Long/PL_M1_098/PL_M1_098_obj.usd",
            "cloth86": self.path
            + "/Assets/Garment/Trousers/Long/PL_pants029/PL_pants029_obj.usd",
            "cloth87": self.path
            + "/Assets/Garment/Trousers/Long/PL_Pants055/PL_Pants055_obj.usd",
            "cloth88": self.path
            + "/Assets/Garment/Trousers/Long/PL_Pants067/PL_Pants067_obj.usd",
            "cloth89": self.path
            + "/Assets/Garment/Trousers/Long/PL_Pants79/PL_Pants79_obj.usd",
            "cloth90": self.path
            + "/Assets/Garment/Trousers/Long/PL_Short019/PL_Short019_obj.usd",
            "cloth91": self.path
            + "/Assets/Garment/Trousers/Short/PL_Pants087/PL_Pants087_obj.usd",
            "cloth92": self.path
            + "/Assets/Garment/Trousers/Short/PS_010/PS_010_obj.usd",
            "cloth93": self.path
            + "/Assets/Garment/Trousers/Short/PS_M1_040/PS_M1_040_obj.usd",
            "cloth94": self.path
            + "/Assets/Garment/Trousers/Short/PS_M1_095/PS_M1_095_obj.usd",
            "cloth95": self.path
            + "/Assets/Garment/Trousers/Short/PS_Short062/PS_Short062_obj.usd",
            "cloth96": self.path
            + "/Assets/Garment/UnderPants/UP_M1_017/UP_M1_017_obj.usd",
            "cloth97": self.path
            + "/Assets/Garment/UnderPants/UP_M1_103/UP_M1_103_obj.usd",
            "cloth98": self.path
            + "/Assets/Garment/UnderPants/UP_Short011/UP_Short011_obj.usd",
            "cloth99": self.path
            + "/Assets/Garment/UnderPants/UP_Short016/UP_Short016_obj.usd",
            "cloth100": self.path
            + "/Assets/Garment/UnderPants/UP_Short095/UP_Short095_obj.usd",
            # big clothes
            "cloth101": self.path
            + "/Assets/Garment/Dress/Long_Gallus/DLG_Dress035_0/DLG_Dress035_0_obj.usd",
            "cloth102": self.path
            + "/Assets/Garment/Dress/Long_ShortSleeve/DLSS_Dress302/DLSS_Dress302_obj.usd",
            "cloth103": self.path
            + "/Assets/Garment/Dress/Long_ShortSleeve/DLSS_Dress356/DLSS_Dress356_obj.usd",
            "cloth104": self.path
            + "/Assets/Garment/Scarf_Tie/ST_Scarf-009/ST_Scarf-009_obj.usd",
            "cloth105": self.path
            + "/Assets/Garment/Dress/Long_LongSleeve/DLLS_Dress17/DLLS_Dress17_obj.usd",
            "cloth106": self.path
            + "/Assets/Garment/Dress/Long_LongSleeve/DLLS_dress230/DLLS_dress230_obj.usd",
            "cloth107": self.path
            + "/Assets/Garment/Tops/Collar_Lsleeve_FrontClose/TCLC_003/TCLC_003_obj.usd",
            "cloth108": self.path
            + "/Assets/Garment/Tops/Collar_Lsleeve_FrontClose/TCLC_016/TCLC_016_obj.usd",
            "cloth109": self.path
            + "/Assets/Garment/Tops/Collar_Lsleeve_FrontOpen/TCLO_022/TCLO_022_obj.usd",
            "cloth110": self.path
            + "/Assets/Garment/Tops/Hooded_Lsleeve_FrontOpen/THLO_Jacket111/THLO_Jacket111_obj.usd",
            "cloth117": self.path
            + "/Assets/Garment/Dress/Long_LongSleeve/DLLS_Dress334/DLLS_Dress334_obj.usd",
            "cloth111": self.path
            + "/Assets/Garment/Tops/Collar_Lsleeve_FrontOpen/TCLO_013_/TCLO_013__obj.usd",
            "cloth112": self.path
            + "/Assets/Garment/Tops/Hooded_Lsleeve_FrontOpen/THLO_Jacket015/THLO_Jacket015_obj.usd",
            "cloth113": self.path
            + "/Assets/Garment/Trousers/Long/PL_003/PL_003_obj.usd",
            "cloth114": self.path
            + "/Assets/Garment/Trousers/Long/PL_058/PL_058_obj.usd",
            "cloth115": self.path
            + "/Assets/Garment/Dress/Long_LongSleeve/DLLS_Dress374/DLLS_Dress374_obj.usd",
            "cloth116": self.path
            + "/Assets/Garment/Trousers/Long/PL_LongPants017/PL_LongPants017_obj.usd",
            # scarf
            "cloth117": self.path
            + "/Assets/Garment/Scarf_Tie/ST_scarf1/ST_scarf1_obj.usd",
            "cloth118": self.path
            + "/Assets/Garment/Scarf_Tie/ST_scarf5/ST_scarf5_obj.usd",
            "cloth119": self.path
            + "/Assets/Garment/Scarf_Tie/ST_scarf9/ST_scarf9_obj.usd",
            "cloth120": self.path
            + "/Assets/Garment/Scarf_Tie/ST_Scarf-001/ST_Scarf-001_obj.usd",
            "cloth121": self.path
            + "/Assets/Garment/Scarf_Tie/ST_Scarf-001/ST_Scarf-001_obj.usd",
            "cloth122": self.path
            + "/Assets/Garment/Scarf_Tie/ST_Scarf-005/ST_Scarf-005_obj.usd",
            "cloth123": self.path
            + "/Assets/Garment/Scarf_Tie/ST_Scarf-009/ST_Scarf-009_obj.usd",
            # dress short-long sleeve
            "cloth124": self.path
            + "/Assets/Garment/Dress/Short_LongSleeve/DLLS_Dress054_1/DLLS_Dress054_1_obj.usd",
            "cloth125": self.path
            + "/Assets/Garment/Dress/Short_LongSleeve/DSLS_dress234/DSLS_dress234_obj.usd",
            "cloth126": self.path
            + "/Assets/Garment/Dress/Short_LongSleeve/DSLS_Dress015/DSLS_Dress015_obj.usd",
            "cloth127": self.path
            + "/Assets/Garment/Dress/Short_LongSleeve/DSLS_Dress149/DSLS_Dress149_obj.usd",
            "cloth128": self.path
            + "/Assets/Garment/Dress/Short_LongSleeve/DSLS_Dress217/DSLS_Dress217_obj.usd",
            "cloth129": self.path
            + "/Assets/Garment/Dress/Short_LongSleeve/DSLS_Dress414/DSLS_Dress414_obj.usd",
            "cloth130": self.path
            + "/Assets/Garment/Dress/Short_LongSleeve/DSLS_Dress418/DSLS_Dress418_obj.usd",
            # dress short-no sleeve
            "cloth131": self.path
            + "/Assets/Garment/Dress/Short_NoSleeve/DSNS_Dress029_0/DSNS_Dress029_0_obj.usd",
            "cloth132": self.path
            + "/Assets/Garment/Dress/Short_NoSleeve/DSNS_Dress045_1/DSNS_Dress045_1_obj.usd",
            "cloth133": self.path
            + "/Assets/Garment/Dress/Short_NoSleeve/DSNS_Dress077/DSNS_Dress077_obj.usd",
            "cloth134": self.path
            + "/Assets/Garment/Dress/Short_NoSleeve/DSNS_Dress120/DSNS_Dress120_obj.usd",
            "cloth135": self.path
            + "/Assets/Garment/Dress/Short_NoSleeve/DSNS_dress145/DSNS_dress145_obj.usd",
            "cloth136": self.path
            + "/Assets/Garment/Dress/Short_NoSleeve/DSNS_Dress170/DSNS_Dress170_obj.usd",
            "cloth137": self.path
            + "/Assets/Garment/Dress/Short_NoSleeve/DSNS_Dress200/DSNS_Dress200_obj.usd",
            "cloth138": self.path
            + "/Assets/Garment/Dress/Short_NoSleeve/DSNS_Dress218/DSNS_Dress218_obj.usd",
            # hat
            "cloth139": self.path
            + "/Assets/Garment/Hat/HA_Hat001_1/HA_Hat001_1_obj.usd",
            # socks
            "cloth140": self.path
            + "/Assets/Garment/Socks/Long/SOL_Socks013/SOL_Socks013_obj.usd",
            # dress
            "cloth141": self.path
            + "/Assets/Garment/Dress/Short_LongSleeve/DSLS_Dress050_0/DSLS_Dress050_0_obj.usd",
            "cloth142": self.path
            + "/Assets/Garment/Dress/Short_NoSleeve/DSNS_Dress115/DSNS_Dress115_obj.usd",
            # small pieces of garments
            "cloth143": self.path
            + "/Assets/Garment/Dress/Long_LongSleeve/DLLS_Dress008_1/DLLS_Dress008_1_obj.usd",
            "cloth144": self.path
            + "/Assets/Garment/Socks/Short/SOS_Socks026/SOS_Socks026_obj.usd",
            "cloth145": self.path
            + "/Assets/Garment/Trousers/Long/PL_090/PL_090_obj.usd",
            "cloth146": self.path
            + "/Assets/Garment/Socks/Mid/SOL_Socks067/SOL_Socks067_obj.usd",
            "cloth147": self.path
            + "/Assets/Garment/Socks/Mid/SOM_Socks023/SOM_Socks023_obj.usd",
            "cloth148": self.path
            + "/Assets/Garment/Trousers/Long/PL_Short019/PL_Short019_obj.usd",
            "cloth149": self.path
            + "/Assets/Garment/Socks/Short/SOS_Socks063/SOS_Socks063_obj.usd",
            "cloth150": self.path
            + "/Assets/Garment/Dress/Long_LongSleeve/DLLS_Dress289/DLLS_Dress289_obj.usd",
            "cloth151": self.path
            + "/Assets/Garment/Dress/Short_LongSleeve/DLLS_Dress054_1/DLLS_Dress054_1_obj.usd",
            "cloth152": self.path + "/Assets/Garment/Hat/HA_Hat012/HA_Hat012_obj.usd",
        }

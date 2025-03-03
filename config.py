class Config:
    def __init__(self):

        # ------------Franka Robot Config------------ #
        self.robot_position = [-0.68, -0.05, 0.11]  # sequence:"XYZ"

        self.robot_orientation = [
            0.0,
            0.0,
            0.0,
        ]  # sequence:"XYZ", input degrees, e.g.[0.0, 0.0, 90.0]

        self.target_positions = [  # franka move positions sequence
            [-0.15, -0.05, 0.55],  # ready to enter washing machine(enter_point_1)
            # [0.0, -0.05, 0.58],   # enter washing machine(enter_point_2 and leave_point_1)
            # [-0.35, -0.05, 0.65],     # leave washing machine(leave_point_2)
            [-0.8, -0.05, 0.85],
            [-1.2, -0.55, 1.1],  # put garment into target position(leave_point_3)
            # [-0.95, -0.65, 1.1]
        ]
        # ------------Washing_Machine Config------------ #
        self.wm_position = [-0.05, 0.0, 0.58]  # sequence:"XYZ"

        self.wm_orientation = [
            0.0,
            0.0,
            0.0,
        ]  # sequence:"XYZ", input degrees, e.g.[0.0, 0.0, 90.0]

        self.wm_scale = [0.8, 0.8, 0.8]  # sequence:"XYZ", e.g.[1.0, 1.0, 1.0]

        self.wm_prim_path = "/World/Wash_Machine"

        # Washing_Machine_Usd_Path(no need to change)
        self.wm_usd_path = (
            "/home/user/garmentIsaac/WashingMachine_usd/washing_machine.usd"
        )

        # ------------Room Config------------ #
        self.room_position = [-3.39737, -1.65851, 0.0]  # sequence:"XYZ"

        self.room_orientation = [
            0.0,
            0.0,
            0.0,
        ]  # sequence:"XYZ", input degrees, e.g.[0.0, 0.0, 90.0]

        self.room_scale = [0.013, 0.013, 0.012]  # sequence:"XYZ", e.g.[1.0, 1.0, 1.0]

        self.room_prim_path = "/World/Room"

        # Washing_Machine_Usd_Path(no need to change)
        self.room_usd_path = "/home/user/garmentIsaac/kitchen/kitchen_final.usd"

        self.busket_usd_path = "/home/user/garmentIsaac/busket/busket.usd"

        self.busket_position = [-1.08, -0.5, 0.1682]  # sequence:"XYZ"

        self.busket_orientation = [
            0.0,
            0.0,
            90.0,
        ]  # sequence:"XYZ", input degrees, e.g.[0.0, 0.0, 90.0]

        self.busket_scale = [0.45, 0.45, 0.45]  # sequence:"XYZ", e.g.[1.0, 1.0, 1.0]

        self.busket_prim_path = "/World/Busket"

        self.base_usd_path = "/home/user/garmentIsaac/base/base_no_physics.usd"

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
        # self.recording_camera_position = [-2.5, -2.8, 0.8]

        # self.recording_camera_orientation = [0, 0, 56]

        self.recording_camera_position = [-4.17, -2.5, 2.2]

        self.recording_camera_orientation = [0, 22, 30]

        # ------------Recording Camera multi Config------------ #
        # self.recording_camera_multi_position=[-0.8,-6.25,0.57]

        # self.recording_camera_multi_orientation=[0,0,95]

        # ------------Garment Config------------ #

        # Please make sure the length of (position/orientation/scale) array
        # exactly match the garment num
        self.garment_num = 4

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

        # Gatment_Usd_Path(no need to change)
        self.clothpath = {
            "cloth0": "/home/user/garmentIsaac/ClothesNetM_usd/Dress/Long_NoSleeve/DLNS_Dress003_0/DLNS_Dress003_0_obj.usd",
            "cloth1": "/home/user/garmentIsaac/ClothesNetM_usd/Scarf_Tie/ST_Scarf-001/ST_Scarf-001_obj.usd",
            "cloth2": "/home/user/garmentIsaac/ClothesNetM_usd/Dress/Long_Gallus/DLG_Dress032_1/DLG_Dress032_1_obj.usd",
            "cloth3": "/home/user/garmentIsaac/ClothesNetM_usd/Tops/Collar_Lsleeve_FrontClose/TCLC_002/TCLC_002_obj.usd",
            "cloth4": "/home/user/garmentIsaac/ClothesNetM_usd/Tops/Collar_Lsleeve_FrontClose/TCLC_015/TCLC_015_obj.usd",
            "cloth5": "/home/user/garmentIsaac/ClothesNetM_usd/Dress/Long_ShortSleeve/DLSS_Dress037_0/DLSS_Dress037_0_obj.usd",
            "cloth6": "/home/user/garmentIsaac/ClothesNetM_usd/Dress/Short_LongSleeve/DSLS_dress271/DSLS_dress271_obj.usd",
            "cloth7": "/home/user/garmentIsaac/ClothesNetM_usd/Skirt/Long/SL_skirt148/SL_skirt148_obj.usd",
            "cloth8": "/home/user/garmentIsaac/ClothesNetM_usd/Skirt/Short/SL_Skirt017_1/SL_Skirt017_1_obj.usd",
            "cloth9": "/home/user/garmentIsaac/ClothesNetM_usd/Scarf_Tie/ST_Tie026/ST_Tie026_obj.usd",
            # Dress-Long_Gallus
            "cloth10": "/home/user/garmentIsaac/ClothesNetM_usd/Dress/Long_Gallus/DLG_Dress035_0/DLG_Dress035_0_obj.usd",
            "cloth11": "/home/user/garmentIsaac/ClothesNetM_usd/Dress/Long_Gallus/DLG_Dress079/DLG_Dress079_obj.usd",
            "cloth12": "/home/user/garmentIsaac/ClothesNetM_usd/Dress/Long_Gallus/DLG_Dress099/DLG_Dress099_obj.usd",
            "cloth13": "/home/user/garmentIsaac/ClothesNetM_usd/Dress/Long_Gallus/DLG_Dress101/DLG_Dress101_obj.usd",
            "cloth14": "/home/user/garmentIsaac/ClothesNetM_usd/Dress/Long_Gallus/DLG_Dress105/DLG_Dress105_obj.usd",
            "cloth15": "/home/user/garmentIsaac/ClothesNetM_usd/Dress/Long_Gallus/DLG_Dress198/DLG_Dress198_obj.usd",
            "cloth16": "/home/user/garmentIsaac/ClothesNetM_usd/Dress/Long_Gallus/DLG_Dress312/DLG_Dress312_obj.usd",
            "cloth17": "/home/user/garmentIsaac/ClothesNetM_usd/Dress/Long_Gallus/DLG_Dress319/DLG_Dress319_obj.usd",
            "cloth18": "/home/user/garmentIsaac/ClothesNetM_usd/Dress/Long_Gallus/DLG_Dress394/DLG_Dress394_obj.usd",
            "cloth19": "/home/user/garmentIsaac/ClothesNetM_usd/Dress/Long_Gallus/DLG_Dress476/DLG_Dress476_obj.usd",
            "cloth20": "/home/user/garmentIsaac/ClothesNetM_usd/Dress/Long_Gallus/DSNS_Dress123/DSNS_Dress123_obj.usd",
            # Dress-LongSleeve
            "cloth21": "/home/user/garmentIsaac/ClothesNetM_usd/Dress/Long_LongSleeve/DLLS_Dress050_1/DLLS_Dress050_1_obj.usd",
            "cloth22": "/home/user/garmentIsaac/ClothesNetM_usd/Dress/Long_LongSleeve/DLLS_dress230/DLLS_dress230_obj.usd",
            "cloth23": "/home/user/garmentIsaac/ClothesNetM_usd/Dress/Long_LongSleeve/DLLS_Dress290/DLLS_Dress290_obj.usd",
            "cloth24": "/home/user/garmentIsaac/ClothesNetM_usd/Dress/Long_LongSleeve/DLLS_Dress333/DLLS_Dress333_obj.usd",
            "cloth25": "/home/user/garmentIsaac/ClothesNetM_usd/Dress/Long_LongSleeve/DLLS_Dress355/DLLS_Dress355_obj.usd",
            # Dress-LongNoSleeve
            "cloth26": "/home/user/garmentIsaac/ClothesNetM_usd/Dress/Long_NoSleeve/DLNS_Dress003_1/DLNS_Dress003_1_obj.usd",
            "cloth27": "/home/user/garmentIsaac/ClothesNetM_usd/Dress/Long_NoSleeve/DLNS_Dress010/DLNS_Dress010_obj.usd",
            "cloth28": "/home/user/garmentIsaac/ClothesNetM_usd/Dress/Long_NoSleeve/DLNS_Dress011/DLNS_Dress011_obj.usd",
            "cloth29": "/home/user/garmentIsaac/ClothesNetM_usd/Dress/Long_NoSleeve/DLNS_Dress021/DLNS_Dress021_obj.usd",
            "cloth30": "/home/user/garmentIsaac/ClothesNetM_usd/Dress/Long_NoSleeve/DLNS_dress040/DLNS_dress040_obj.usd",
            "cloth31": "/home/user/garmentIsaac/ClothesNetM_usd/Dress/Long_NoSleeve/DLNS_Dress131/DLNS_Dress131_obj.usd",
            "cloth32": "/home/user/garmentIsaac/ClothesNetM_usd/Dress/Long_NoSleeve/DLNS_Dress240/DLNS_Dress240_obj.usd",
            "cloth33": "/home/user/garmentIsaac/ClothesNetM_usd/Dress/Long_NoSleeve/DLNS_Dress291/DLNS_Dress291_obj.usd",
            "cloth34": "/home/user/garmentIsaac/ClothesNetM_usd/Dress/Long_NoSleeve/DSNS_Dress049_1/DSNS_Dress049_1_obj.usd",
            "cloth35": "/home/user/garmentIsaac/ClothesNetM_usd/Dress/Long_NoSleeve/DLNS_Dress030/DLNS_Dress030_obj.usd",
            # Dress-LongShortSleeve
            "cloth36": "/home/user/garmentIsaac/ClothesNetM_usd/Dress/Long_ShortSleeve/DLSS_Dress051_1/DLSS_Dress051_1_obj.usd",
            "cloth37": "/home/user/garmentIsaac/ClothesNetM_usd/Dress/Long_ShortSleeve/DLSS_Dress356/DLSS_Dress356_obj.usd",
            # Dress-LongTube
            "cloth38": "/home/user/garmentIsaac/ClothesNetM_usd/Dress/Long_Tube/DLT_Dress036_0/DLT_Dress036_0_obj.usd",
            "cloth39": "/home/user/garmentIsaac/ClothesNetM_usd/Dress/Long_Tube/DLT_Dress389/DLT_Dress389_obj.usd",
            # Dress-ShortGallus
            "cloth40": "/home/user/garmentIsaac/ClothesNetM_usd/Dress/Short_Gallus/DSG_Dress102/DSG_Dress102_obj.usd",
            "cloth41": "/home/user/garmentIsaac/ClothesNetM_usd/Dress/Short_Gallus/DSNS_Dress193/DSNS_Dress193_obj.usd",
            # one-piece
            "cloth42": "/home/user/garmentIsaac/ClothesNetM_usd/One-piece/OP_Overall006/OP_Overall006_obj.usd",
            "cloth43": "/home/user/garmentIsaac/ClothesNetM_usd/One-piece/OP_Overall015/OP_Overall015_obj.usd",
            "cloth44": "/home/user/garmentIsaac/ClothesNetM_usd/One-piece/OP_overall033/OP_overall033_obj.usd",
            "cloth45": "/home/user/garmentIsaac/ClothesNetM_usd/One-piece/OP_Overall055/OP_Overall055_obj.usd",
            "cloth46": "/home/user/garmentIsaac/ClothesNetM_usd/One-piece/OP_Overall094/OP_Overall094_obj.usd",
            "cloth47": "/home/user/garmentIsaac/ClothesNetM_usd/One-piece/OP_Overall123/OP_Overall123_obj.usd",
            # long-skirt
            "cloth48": "/home/user/garmentIsaac/ClothesNetM_usd/Skirt/Long/SL_skirt023/SL_skirt023_obj.usd",
            "cloth49": "/home/user/garmentIsaac/ClothesNetM_usd/Skirt/Long/SL_Skirt096/SL_Skirt096_obj.usd",
            "cloth50": "/home/user/garmentIsaac/ClothesNetM_usd/Skirt/Long/SL_Skirt248/SL_Skirt248_obj.usd",
            "cloth51": "/home/user/garmentIsaac/ClothesNetM_usd/Skirt/Long/SL_Skirt258/SL_Skirt258_obj.usd",
            "cloth52": "/home/user/garmentIsaac/ClothesNetM_usd/Skirt/Long/SL_skirt293/SL_skirt293_obj.usd",
            "cloth53": "/home/user/garmentIsaac/ClothesNetM_usd/Skirt/Long/SL_Skirt366/SL_Skirt366_obj.usd",
            # short-skirt
            "cloth54": "/home/user/garmentIsaac/ClothesNetM_usd/Skirt/Short/SS_Skirt029/SS_Skirt029_obj.usd",
            "cloth55": "/home/user/garmentIsaac/ClothesNetM_usd/Skirt/Short/SS_Skirt074/SS_Skirt074_obj.usd",
            "cloth56": "/home/user/garmentIsaac/ClothesNetM_usd/Skirt/Short/SS_Skirt086/SS_Skirt086_obj.usd",
            "cloth57": "/home/user/garmentIsaac/ClothesNetM_usd/Skirt/Short/SS_Skirt142/SS_Skirt142_obj.usd",
            "cloth58": "/home/user/garmentIsaac/ClothesNetM_usd/Skirt/Short/SS_Skirt265/SS_Skirt265_obj.usd",
            "cloth59": "/home/user/garmentIsaac/ClothesNetM_usd/Skirt/Short/SS_Skirt368/SS_Skirt368_obj.usd",
            # tops
            "cloth60": "/home/user/garmentIsaac/ClothesNetM_usd/Tops/Collar_Lsleeve_FrontClose/TCLC_014/TCLC_014_obj.usd",
            "cloth61": "/home/user/garmentIsaac/ClothesNetM_usd/Tops/Collar_Lsleeve_FrontClose/TCLC_Top566/TCLC_Top566_obj.usd",
            "cloth62": "/home/user/garmentIsaac/ClothesNetM_usd/Tops/Collar_Lsleeve_FrontOpen/TCLO_048/TCLO_048_obj.usd",
            "cloth63": "/home/user/garmentIsaac/ClothesNetM_usd/Tops/Collar_Lsleeve_FrontOpen/TCLO_Jacket134/TCLO_Jacket134_obj.usd",
            "cloth64": "/home/user/garmentIsaac/ClothesNetM_usd/Tops/Collar_Lsleeve_FrontOpen/TCLO_Normal_Model_057/TCLO_Normal_Model_057_obj.usd",
            "cloth65": "/home/user/garmentIsaac/ClothesNetM_usd/Tops/Collar_noSleeve_FrontClose/TCNC_model2_033/TCNC_model2_033_obj.usd",
            "cloth66": "/home/user/garmentIsaac/ClothesNetM_usd/Tops/Collar_noSleeve_FrontClose/TCNC_Top086/TCNC_Top086_obj.usd",
            "cloth67": "/home/user/garmentIsaac/ClothesNetM_usd/Tops/Collar_Ssleeve_FrontClose/TCSC_Jacket167/TCSC_Jacket167_obj.usd",
            "cloth68": "/home/user/garmentIsaac/ClothesNetM_usd/Tops/Collar_Ssleeve_FrontClose/TCSC_polo004/TCSC_polo004_obj.usd",
            "cloth69": "/home/user/garmentIsaac/ClothesNetM_usd/Tops/NoCollar_Lsleeve_FrontClose/TNLC_010/TNLC_010_obj.usd",
            "cloth70": "/home/user/garmentIsaac/ClothesNetM_usd/Tops/NoCollar_Lsleeve_FrontClose/TNLC_Jumper002/TNLC_Jumper002_obj.usd",
            "cloth71": "/home/user/garmentIsaac/ClothesNetM_usd/Tops/NoCollar_Lsleeve_FrontClose/TNLC_top189/TNLC_top189_obj.usd",
            "cloth72": "/home/user/garmentIsaac/ClothesNetM_usd/Tops/NoCollar_Lsleeve_FrontClose/TNLC_Top400/TNLC_Top400_obj.usd",
            "cloth73": "/home/user/garmentIsaac/ClothesNetM_usd/Tops/NoCollar_Lsleeve_FrontClose/TNLC_Top425/TNLC_Top425_obj.usd",
            "cloth74": "/home/user/garmentIsaac/ClothesNetM_usd/Tops/NoCollar_Lsleeve_FrontClose/TNLC_Top504/TNLC_Top504_obj.usd",
            "cloth75": "/home/user/garmentIsaac/ClothesNetM_usd/Tops/NoCollar_Lsleeve_FrontClose/TNLC_Top550/TNLC_Top550_obj.usd",
            "cloth76": "/home/user/garmentIsaac/ClothesNetM_usd/Tops/NoCollar_Ssleeve_FrontClose/TNSC_Top626/TNSC_Top626_obj.usd",
            "cloth77": "/home/user/garmentIsaac/ClothesNetM_usd/Tops/NoCollar_Ssleeve_FrontOpen/TNSO_model2_052/TNSO_model2_052_obj.usd",
            # trousers
            "cloth78": "/home/user/garmentIsaac/ClothesNetM_usd/Trousers/Long/PL_030/PL_030_obj.usd",
            "cloth79": "/home/user/garmentIsaac/ClothesNetM_usd/Trousers/Long/PL_047/PL_047_obj.usd",
            "cloth80": "/home/user/garmentIsaac/ClothesNetM_usd/Trousers/Long/PL_071/PL_071_obj.usd",
            "cloth81": "/home/user/garmentIsaac/ClothesNetM_usd/Trousers/Long/PL_LongPants003/PL_LongPants003_obj.usd",
            "cloth82": "/home/user/garmentIsaac/ClothesNetM_usd/Trousers/Long/PL_M1_005/PL_M1_005_obj.usd",
            "cloth83": "/home/user/garmentIsaac/ClothesNetM_usd/Trousers/Long/PL_M1_024/PL_M1_024_obj.usd",
            "cloth84": "/home/user/garmentIsaac/ClothesNetM_usd/Trousers/Long/PL_M1_056/PL_M1_056_obj.usd",
            "cloth85": "/home/user/garmentIsaac/ClothesNetM_usd/Trousers/Long/PL_M1_098/PL_M1_098_obj.usd",
            "cloth86": "/home/user/garmentIsaac/ClothesNetM_usd/Trousers/Long/PL_pants029/PL_pants029_obj.usd",
            "cloth87": "/home/user/garmentIsaac/ClothesNetM_usd/Trousers/Long/PL_Pants055/PL_Pants055_obj.usd",
            "cloth88": "/home/user/garmentIsaac/ClothesNetM_usd/Trousers/Long/PL_Pants067/PL_Pants067_obj.usd",
            "cloth89": "/home/user/garmentIsaac/ClothesNetM_usd/Trousers/Long/PL_Pants79/PL_Pants79_obj.usd",
            "cloth90": "/home/user/garmentIsaac/ClothesNetM_usd/Trousers/Long/PL_Short019/PL_Short019_obj.usd",
            "cloth91": "/home/user/garmentIsaac/ClothesNetM_usd/Trousers/Short/PL_Pants087/PL_Pants087_obj.usd",
            "cloth92": "/home/user/garmentIsaac/ClothesNetM_usd/Trousers/Short/PS_010/PS_010_obj.usd",
            "cloth93": "/home/user/garmentIsaac/ClothesNetM_usd/Trousers/Short/PS_M1_040/PS_M1_040_obj.usd",
            "cloth94": "/home/user/garmentIsaac/ClothesNetM_usd/Trousers/Short/PS_M1_095/PS_M1_095_obj.usd",
            "cloth95": "/home/user/garmentIsaac/ClothesNetM_usd/Trousers/Short/PS_Short062/PS_Short062_obj.usd",
            "cloth96": "/home/user/garmentIsaac/ClothesNetM_usd/UnderPants/UP_M1_017/UP_M1_017_obj.usd",
            "cloth97": "/home/user/garmentIsaac/ClothesNetM_usd/UnderPants/UP_M1_103/UP_M1_103_obj.usd",
            "cloth98": "/home/user/garmentIsaac/ClothesNetM_usd/UnderPants/UP_Short011/UP_Short011_obj.usd",
            "cloth99": "/home/user/garmentIsaac/ClothesNetM_usd/UnderPants/UP_Short016/UP_Short016_obj.usd",
            "cloth100": "/home/user/garmentIsaac/ClothesNetM_usd/UnderPants/UP_Short095/UP_Short095_obj.usd",
            # big clothes
            "cloth101": "/home/user/garmentIsaac/ClothesNetM_usd/Dress/Long_Gallus/DLG_Dress035_0/DLG_Dress035_0_obj.usd",
            "cloth102": "/home/user/garmentIsaac/ClothesNetM_usd/Dress/Long_ShortSleeve/DLSS_Dress302/DLSS_Dress302_obj.usd",
            "cloth103": "/home/user/garmentIsaac/ClothesNetM_usd/Dress/Long_ShortSleeve/DLSS_Dress356/DLSS_Dress356_obj.usd",
            "cloth104": "/home/user/garmentIsaac/ClothesNetM_usd/Scarf_Tie/ST_Scarf-009/ST_Scarf-009_obj.usd",
            "cloth105": "/home/user/garmentIsaac/ClothesNetM_usd/Dress/Long_LongSleeve/DLLS_Dress17/DLLS_Dress17_obj.usd",
            "cloth106": "/home/user/garmentIsaac/ClothesNetM_usd/Dress/Long_LongSleeve/DLLS_dress230/DLLS_dress230_obj.usd",
            "cloth107": "/home/user/garmentIsaac/ClothesNetM_usd/Tops/Collar_Lsleeve_FrontClose/TCLC_003/TCLC_003_obj.usd",
            "cloth108": "/home/user/garmentIsaac/ClothesNetM_usd/Tops/Collar_Lsleeve_FrontClose/TCLC_016/TCLC_016_obj.usd",
            "cloth109": "/home/user/garmentIsaac/ClothesNetM_usd/Tops/Collar_Lsleeve_FrontOpen/TCLO_022/TCLO_022_obj.usd",
            "cloth110": "/home/user/garmentIsaac/ClothesNetM_usd/Tops/Hooded_Lsleeve_FrontOpen/THLO_Jacket111/THLO_Jacket111_obj.usd",
            "cloth117": "/home/user/garmentIsaac/ClothesNetM_usd/Dress/Long_LongSleeve/DLLS_Dress334/DLLS_Dress334_obj.usd",
            "cloth111": "/home/user/garmentIsaac/ClothesNetM_usd/Tops/Collar_Lsleeve_FrontOpen/TCLO_013_/TCLO_013__obj.usd",
            "cloth112": "/home/user/garmentIsaac/ClothesNetM_usd/Tops/Hooded_Lsleeve_FrontOpen/THLO_Jacket015/THLO_Jacket015_obj.usd",
            "cloth113": "/home/user/garmentIsaac/ClothesNetM_usd/Trousers/Long/PL_003/PL_003_obj.usd",
            "cloth114": "/home/user/garmentIsaac/ClothesNetM_usd/Trousers/Long/PL_058/PL_058_obj.usd",
            "cloth115": "/home/user/garmentIsaac/ClothesNetM_usd/Dress/Long_LongSleeve/DLLS_Dress374/DLLS_Dress374_obj.usd",
            "cloth116": "/home/user/garmentIsaac/ClothesNetM_usd/Trousers/Long/PL_LongPants017/PL_LongPants017_obj.usd",
            # scarf
            "cloth117": "/home/user/garmentIsaac/ClothesNetM_usd/Scarf_Tie/ST_scarf1/ST_scarf1_obj.usd",
            "cloth118": "/home/user/garmentIsaac/ClothesNetM_usd/Scarf_Tie/ST_scarf5/ST_scarf5_obj.usd",
            "cloth119": "/home/user/garmentIsaac/ClothesNetM_usd/Scarf_Tie/ST_scarf9/ST_scarf9_obj.usd",
            "cloth120": "/home/user/garmentIsaac/ClothesNetM_usd/Scarf_Tie/ST_Scarf-001/ST_Scarf-001_obj.usd",
            "cloth121": "/home/user/garmentIsaac/ClothesNetM_usd/Scarf_Tie/ST_Scarf-001/ST_Scarf-001_obj.usd",
            "cloth122": "/home/user/garmentIsaac/ClothesNetM_usd/Scarf_Tie/ST_Scarf-005/ST_Scarf-005_obj.usd",  #### 红围巾
            "cloth123": "/home/user/garmentIsaac/ClothesNetM_usd/Scarf_Tie/ST_Scarf-009/ST_Scarf-009_obj.usd",
            # dress short-long sleeve
            "cloth124": "/home/user/garmentIsaac/ClothesNetM_usd/Dress/Short_LongSleeve/DLLS_Dress054_1/DLLS_Dress054_1_obj.usd",
            "cloth125": "/home/user/garmentIsaac/ClothesNetM_usd/Dress/Short_LongSleeve/DSLS_dress234/DSLS_dress234_obj.usd",
            "cloth126": "/home/user/garmentIsaac/ClothesNetM_usd/Dress/Short_LongSleeve/DSLS_Dress015/DSLS_Dress015_obj.usd",
            "cloth127": "/home/user/garmentIsaac/ClothesNetM_usd/Dress/Short_LongSleeve/DSLS_Dress149/DSLS_Dress149_obj.usd",
            "cloth128": "/home/user/garmentIsaac/ClothesNetM_usd/Dress/Short_LongSleeve/DSLS_Dress217/DSLS_Dress217_obj.usd",
            "cloth129": "/home/user/garmentIsaac/ClothesNetM_usd/Dress/Short_LongSleeve/DSLS_Dress414/DSLS_Dress414_obj.usd",
            "cloth130": "/home/user/garmentIsaac/ClothesNetM_usd/Dress/Short_LongSleeve/DSLS_Dress418/DSLS_Dress418_obj.usd",
            # dress short-no sleeve
            "cloth131": "/home/user/garmentIsaac/ClothesNetM_usd/Dress/Short_NoSleeve/DSNS_Dress029_0/DSNS_Dress029_0_obj.usd",  ### 淡蓝裙摆礼裙
            "cloth132": "/home/user/garmentIsaac/ClothesNetM_usd/Dress/Short_NoSleeve/DSNS_Dress045_1/DSNS_Dress045_1_obj.usd",
            "cloth133": "/home/user/garmentIsaac/ClothesNetM_usd/Dress/Short_NoSleeve/DSNS_Dress077/DSNS_Dress077_obj.usd",
            "cloth134": "/home/user/garmentIsaac/ClothesNetM_usd/Dress/Short_NoSleeve/DSNS_Dress120/DSNS_Dress120_obj.usd",
            "cloth135": "/home/user/garmentIsaac/ClothesNetM_usd/Dress/Short_NoSleeve/DSNS_dress145/DSNS_dress145_obj.usd",
            "cloth136": "/home/user/garmentIsaac/ClothesNetM_usd/Dress/Short_NoSleeve/DSNS_Dress170/DSNS_Dress170_obj.usd",
            "cloth137": "/home/user/garmentIsaac/ClothesNetM_usd/Dress/Short_NoSleeve/DSNS_Dress200/DSNS_Dress200_obj.usd",
            "cloth138": "/home/user/garmentIsaac/ClothesNetM_usd/Dress/Short_NoSleeve/DSNS_Dress218/DSNS_Dress218_obj.usd",
            # hat
            "cloth139": "/home/user/garmentIsaac/ClothesNetM_usd/Hat/HA_Hat001_1/HA_Hat001_1_obj.usd",
            # socks
            "cloth140": "/home/user/garmentIsaac/ClothesNetM_usd/Socks/Long/SOL_Socks013/SOL_Socks013_obj.usd",
            # dress 豪堪的
            "cloth141": "/home/user/garmentIsaac/ClothesNetM_usd/Dress/Short_LongSleeve/DSLS_Dress050_0/DSLS_Dress050_0_obj.usd",
            "cloth142": "/home/user/garmentIsaac/ClothesNetM_usd/Dress/Short_NoSleeve/DSNS_Dress115/DSNS_Dress115_obj.usd",
            # 垫的
            "cloth143": "/home/user/garmentIsaac/ClothesNetM_usd/Dress/Long_LongSleeve/DLLS_Dress008_1/DLLS_Dress008_1_obj.usd",
            "cloth144": "/home/user/garmentIsaac/ClothesNetM_usd/Socks/Short/SOS_Socks026/SOS_Socks026_obj.usd",  ### 小短袜
            "cloth145": "/home/user/garmentIsaac/ClothesNetM_usd/Trousers/Long/PL_090/PL_090_obj.usd",  ### 淡蓝色裤子
            "cloth146": "/home/user/garmentIsaac/ClothesNetM_usd/Socks/Mid/SOL_Socks067/SOL_Socks067_obj.usd",  ### 中筒黑袜
            "cloth147": "/home/user/garmentIsaac/ClothesNetM_usd/Socks/Mid/SOM_Socks023/SOM_Socks023_obj.usd",  ### 中筒白袜
            "cloth148": "/home/user/garmentIsaac/ClothesNetM_usd/Trousers/Long/PL_Short019/PL_Short019_obj.usd",  ### 格子短裤
            "cloth149": "/home/user/garmentIsaac/ClothesNetM_usd/Socks/Short/SOS_Socks063/SOS_Socks063_obj.usd",  ### 灰色短袜
            "cloth150": "/home/user/garmentIsaac/ClothesNetM_usd/Dress/Long_LongSleeve/DLLS_Dress289/DLLS_Dress289_obj.usd",  ### 粉白长袖连衣裙
            "cloth151": "/home/user/garmentIsaac/ClothesNetM_usd/Dress/Short_LongSleeve/DLLS_Dress054_1/DLLS_Dress054_1_obj.usd",  ### 碎花裙子
            "cloth152": "/home/user/garmentIsaac/ClothesNetM_usd/Hat/HA_Hat012/HA_Hat012_obj.usd",  ### 红色帽子
        }

    def get_replicator_robot(self):
        robot_pos = []
        for i in range(-2, 3):
            for j in range(-2, 3):
                pos = []
                pos.append(self.robot_position[0] + i * 2)
                pos.append(self.robot_position[1] + j * 2)
                pos.append(self.robot_position[2])
                robot_pos.append(pos)

        return robot_pos

    def get_replicator_wm(self):
        wm_pos = []
        for i in range(-2, 3):
            for j in range(-2, 3):
                pos = []
                pos.append(self.wm_position[0] + i * 2)
                pos.append(self.wm_position[1] + j * 2)
                pos.append(self.wm_position[2])
                wm_pos.append(pos)

        return wm_pos

    def get_replicator_garment(self):
        garment_pos = []
        for i in range(-2, 3):
            for j in range(-2, 3):
                g_pos = []
                for k in range(self.garment_num):
                    pos = []
                    pos.append(self.garment_position[k][0] + i * 2)
                    pos.append(self.garment_position[k][1] + j * 2)
                    pos.append(self.garment_position[k][2])
                    g_pos.append(pos)
                garment_pos.append(g_pos)

        return garment_pos

    def get_replicator_pc(self):
        wm_pos = []
        for i in range(-2, 3):
            for j in range(-2, 3):
                pos = []
                pos.append(self.point_cloud_camera_position[0] + i * 2)
                pos.append(self.point_cloud_camera_position[1] + j * 2)
                pos.append(self.point_cloud_camera_position[2])
                wm_pos.append(pos)

        return wm_pos

    def get_replicator_rc(self):
        wm_pos = []
        for i in range(-2, 3):
            for j in range(-2, 3):
                pos = []
                pos.append(self.recording_camera_position[0] + i * 2)
                pos.append(self.recording_camera_position[1] + j * 2)
                pos.append(self.recording_camera_position[2])
                wm_pos.append(pos)

        return wm_pos

    def get_replicator_tp(self):
        target_pos = []
        for i in range(-2, 3):
            for j in range(-2, 3):
                t_pos = []
                for k in range(len(self.target_positions)):
                    pos = []
                    pos.append(self.target_positions[k][0] + i * 2)
                    pos.append(self.target_positions[k][1] + j * 2)
                    pos.append(self.target_positions[k][2])
                    t_pos.append(pos)
                target_pos.append(t_pos)

        return target_pos

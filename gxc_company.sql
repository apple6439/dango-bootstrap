/*
 Navicat Premium Data Transfer

 Source Server         : gxc
 Source Server Type    : MySQL
 Source Server Version : 80031
 Source Host           : localhost:3306
 Source Schema         : gxc_company

 Target Server Type    : MySQL
 Target Server Version : 80031
 File Encoding         : 65001

 Date: 03/12/2024 16:39:57
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for app01_admin
-- ----------------------------
DROP TABLE IF EXISTS `app01_admin`;
CREATE TABLE `app01_admin`  (
  `admin_id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `password` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `admin_image` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `email` varchar(254) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  PRIMARY KEY (`admin_id`) USING BTREE,
  UNIQUE INDEX `email`(`email`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 5 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of app01_admin
-- ----------------------------
INSERT INTO `app01_admin` VALUES (1, 'admin', '123456', 'admins/potato.jpeg', '1411992843@qq.com');
INSERT INTO `app01_admin` VALUES (2, 'test', '123456', 'admins/admin_img.jpeg', '1411992842@qq.com');
INSERT INTO `app01_admin` VALUES (5, 'test02', '123456', 'admins/admin_img.jpeg', '1411992841@qq.com');
INSERT INTO `app01_admin` VALUES (6, 'test03', '123456', 'admins/admin_img.jpeg', '1411992844@qq.com');
INSERT INTO `app01_admin` VALUES (7, 'test04', '123456', 'admins/admin_img.jpeg', '1411992845@qq.com');

-- ----------------------------
-- Table structure for app01_department
-- ----------------------------
DROP TABLE IF EXISTS `app01_department`;
CREATE TABLE `app01_department`  (
  `department_id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `performance` decimal(10, 2) NOT NULL,
  `parent_department_id` int NULL DEFAULT NULL,
  `manager_id` int NULL DEFAULT NULL,
  PRIMARY KEY (`department_id`) USING BTREE,
  INDEX `app01_department_manager_id_7f2069df_fk_app01_emp`(`manager_id`) USING BTREE,
  INDEX `app01_department_parent_department_id_0000e29e_fk_app01_dep`(`parent_department_id`) USING BTREE,
  CONSTRAINT `app01_department_manager_id_7f2069df_fk_app01_emp` FOREIGN KEY (`manager_id`) REFERENCES `app01_employee` (`employee_id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `app01_department_parent_department_id_0000e29e_fk_app01_dep` FOREIGN KEY (`parent_department_id`) REFERENCES `app01_department` (`department_id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 13 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of app01_department
-- ----------------------------
INSERT INTO `app01_department` VALUES (1, '北京总部', '2004-06-16 16:29:55.000000', 3453656.00, NULL, 1);
INSERT INTO `app01_department` VALUES (2, '河北分部', '2005-06-16 16:31:46.000000', 435456.00, 1, 1);
INSERT INTO `app01_department` VALUES (3, '保定分部', '2021-07-30 16:32:30.000000', 435435.00, 2, 1);
INSERT INTO `app01_department` VALUES (4, '河南分部', '2020-06-19 00:00:00.000000', 435453.00, 1, NULL);
INSERT INTO `app01_department` VALUES (5, '天津分部', '2020-02-06 00:00:00.000000', 535423.00, 1, 1);
INSERT INTO `app01_department` VALUES (7, '黑龙江分部', '2011-05-12 00:00:00.000000', 9348534.00, 1, 1);
INSERT INTO `app01_department` VALUES (8, '江西分部', '2024-11-06 00:00:00.000000', 4564564.00, 1, 1);
INSERT INTO `app01_department` VALUES (12, '山西分部', '2010-11-04 00:00:00.000000', 5464646.00, 1, 1);

-- ----------------------------
-- Table structure for app01_employee
-- ----------------------------
DROP TABLE IF EXISTS `app01_employee`;
CREATE TABLE `app01_employee`  (
  `employee_id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `gender` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `hire_date` date NOT NULL,
  `salary` decimal(10, 2) NOT NULL,
  `department_id` int NOT NULL,
  PRIMARY KEY (`employee_id`) USING BTREE,
  INDEX `app01_employee_department_id_96795f93_fk_app01_dep`(`department_id`) USING BTREE,
  CONSTRAINT `app01_employee_department_id_96795f93_fk_app01_dep` FOREIGN KEY (`department_id`) REFERENCES `app01_department` (`department_id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 9 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of app01_employee
-- ----------------------------
INSERT INTO `app01_employee` VALUES (1, '高薪春', '0', '2015-03-19', 32107.00, 1);
INSERT INTO `app01_employee` VALUES (2, '高薪秋', '1', '2024-10-29', 1023.00, 5);
INSERT INTO `app01_employee` VALUES (5, '高薪秋', '1', '2024-10-29', 10233.00, 5);
INSERT INTO `app01_employee` VALUES (7, '高薪夏', '0', '2024-12-02', 23238.00, 4);
INSERT INTO `app01_employee` VALUES (8, '高薪冬', '1', '2024-12-17', 12124.00, 3);

-- ----------------------------
-- Table structure for app01_order
-- ----------------------------
DROP TABLE IF EXISTS `app01_order`;
CREATE TABLE `app01_order`  (
  `order_id` int NOT NULL AUTO_INCREMENT,
  `product_image` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `product_name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `quantity` int UNSIGNED NOT NULL,
  `customer_name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `order_date` datetime(6) NOT NULL,
  PRIMARY KEY (`order_id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 17 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of app01_order
-- ----------------------------
INSERT INTO `app01_order` VALUES (1, 'product_images/tomato.png', '西红柿', 32465, '河北大学', '2024-11-27 04:09:00.000000');
INSERT INTO `app01_order` VALUES (8, 'product_images/potato.jpeg', '土豆', 54645, '华北电力大学', '2024-11-27 04:09:00.000000');
INSERT INTO `app01_order` VALUES (12, 'product_images/黄瓜.jpg', '黄瓜', 9943, '河北大学', '2024-12-02 12:03:00.000000');
INSERT INTO `app01_order` VALUES (13, 'product_images/黄瓜_ifQmAoc.jpg', '黄瓜', 432, '河北农业大学', '2024-12-02 15:46:00.000000');
INSERT INTO `app01_order` VALUES (14, 'product_images/白菜.webp', '白菜', 28649, '燕山大学', '2024-12-03 03:06:00.000000');
INSERT INTO `app01_order` VALUES (15, 'product_images/potato_9kKMM6G.jpeg', '土豆', 45672, '河北工业大学', '2024-12-03 03:08:00.000000');
INSERT INTO `app01_order` VALUES (16, 'product_images/白菜_skuSBnm.webp', '白菜', 7234, '石家庄铁道大学', '2024-12-03 03:08:00.000000');
INSERT INTO `app01_order` VALUES (17, 'product_images/豆角_ZKt1qD1.webp', '豆角', 32341, '华北理工大学', '2024-12-03 07:24:00.000000');
INSERT INTO `app01_order` VALUES (19, 'product_images/豆角.webp', '豆角', 3213, '河北师范大学', '2024-12-03 07:26:00.000000');

-- ----------------------------
-- Table structure for auth_group
-- ----------------------------
DROP TABLE IF EXISTS `auth_group`;
CREATE TABLE `auth_group`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `name`(`name`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of auth_group
-- ----------------------------

-- ----------------------------
-- Table structure for auth_group_permissions
-- ----------------------------
DROP TABLE IF EXISTS `auth_group_permissions`;
CREATE TABLE `auth_group_permissions`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `auth_group_permissions_group_id_permission_id_0cd325b0_uniq`(`group_id`, `permission_id`) USING BTREE,
  INDEX `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm`(`permission_id`) USING BTREE,
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of auth_group_permissions
-- ----------------------------

-- ----------------------------
-- Table structure for auth_permission
-- ----------------------------
DROP TABLE IF EXISTS `auth_permission`;
CREATE TABLE `auth_permission`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `auth_permission_content_type_id_codename_01ab375a_uniq`(`content_type_id`, `codename`) USING BTREE,
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 41 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of auth_permission
-- ----------------------------
INSERT INTO `auth_permission` VALUES (1, 'Can add log entry', 1, 'add_logentry');
INSERT INTO `auth_permission` VALUES (2, 'Can change log entry', 1, 'change_logentry');
INSERT INTO `auth_permission` VALUES (3, 'Can delete log entry', 1, 'delete_logentry');
INSERT INTO `auth_permission` VALUES (4, 'Can view log entry', 1, 'view_logentry');
INSERT INTO `auth_permission` VALUES (5, 'Can add permission', 2, 'add_permission');
INSERT INTO `auth_permission` VALUES (6, 'Can change permission', 2, 'change_permission');
INSERT INTO `auth_permission` VALUES (7, 'Can delete permission', 2, 'delete_permission');
INSERT INTO `auth_permission` VALUES (8, 'Can view permission', 2, 'view_permission');
INSERT INTO `auth_permission` VALUES (9, 'Can add group', 3, 'add_group');
INSERT INTO `auth_permission` VALUES (10, 'Can change group', 3, 'change_group');
INSERT INTO `auth_permission` VALUES (11, 'Can delete group', 3, 'delete_group');
INSERT INTO `auth_permission` VALUES (12, 'Can view group', 3, 'view_group');
INSERT INTO `auth_permission` VALUES (13, 'Can add user', 4, 'add_user');
INSERT INTO `auth_permission` VALUES (14, 'Can change user', 4, 'change_user');
INSERT INTO `auth_permission` VALUES (15, 'Can delete user', 4, 'delete_user');
INSERT INTO `auth_permission` VALUES (16, 'Can view user', 4, 'view_user');
INSERT INTO `auth_permission` VALUES (17, 'Can add content type', 5, 'add_contenttype');
INSERT INTO `auth_permission` VALUES (18, 'Can change content type', 5, 'change_contenttype');
INSERT INTO `auth_permission` VALUES (19, 'Can delete content type', 5, 'delete_contenttype');
INSERT INTO `auth_permission` VALUES (20, 'Can view content type', 5, 'view_contenttype');
INSERT INTO `auth_permission` VALUES (21, 'Can add session', 6, 'add_session');
INSERT INTO `auth_permission` VALUES (22, 'Can change session', 6, 'change_session');
INSERT INTO `auth_permission` VALUES (23, 'Can delete session', 6, 'delete_session');
INSERT INTO `auth_permission` VALUES (24, 'Can view session', 6, 'view_session');
INSERT INTO `auth_permission` VALUES (25, 'Can add order', 7, 'add_order');
INSERT INTO `auth_permission` VALUES (26, 'Can change order', 7, 'change_order');
INSERT INTO `auth_permission` VALUES (27, 'Can delete order', 7, 'delete_order');
INSERT INTO `auth_permission` VALUES (28, 'Can view order', 7, 'view_order');
INSERT INTO `auth_permission` VALUES (29, 'Can add department', 8, 'add_department');
INSERT INTO `auth_permission` VALUES (30, 'Can change department', 8, 'change_department');
INSERT INTO `auth_permission` VALUES (31, 'Can delete department', 8, 'delete_department');
INSERT INTO `auth_permission` VALUES (32, 'Can view department', 8, 'view_department');
INSERT INTO `auth_permission` VALUES (33, 'Can add employee', 9, 'add_employee');
INSERT INTO `auth_permission` VALUES (34, 'Can change employee', 9, 'change_employee');
INSERT INTO `auth_permission` VALUES (35, 'Can delete employee', 9, 'delete_employee');
INSERT INTO `auth_permission` VALUES (36, 'Can view employee', 9, 'view_employee');
INSERT INTO `auth_permission` VALUES (37, 'Can add admin', 10, 'add_admin');
INSERT INTO `auth_permission` VALUES (38, 'Can change admin', 10, 'change_admin');
INSERT INTO `auth_permission` VALUES (39, 'Can delete admin', 10, 'delete_admin');
INSERT INTO `auth_permission` VALUES (40, 'Can view admin', 10, 'view_admin');

-- ----------------------------
-- Table structure for auth_user
-- ----------------------------
DROP TABLE IF EXISTS `auth_user`;
CREATE TABLE `auth_user`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `password` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `last_login` datetime(6) NULL DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `first_name` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `last_name` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `email` varchar(254) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `username`(`username`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of auth_user
-- ----------------------------

-- ----------------------------
-- Table structure for auth_user_groups
-- ----------------------------
DROP TABLE IF EXISTS `auth_user_groups`;
CREATE TABLE `auth_user_groups`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `auth_user_groups_user_id_group_id_94350c0c_uniq`(`user_id`, `group_id`) USING BTREE,
  INDEX `auth_user_groups_group_id_97559544_fk_auth_group_id`(`group_id`) USING BTREE,
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of auth_user_groups
-- ----------------------------

-- ----------------------------
-- Table structure for auth_user_user_permissions
-- ----------------------------
DROP TABLE IF EXISTS `auth_user_user_permissions`;
CREATE TABLE `auth_user_user_permissions`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq`(`user_id`, `permission_id`) USING BTREE,
  INDEX `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm`(`permission_id`) USING BTREE,
  CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of auth_user_user_permissions
-- ----------------------------

-- ----------------------------
-- Table structure for django_admin_log
-- ----------------------------
DROP TABLE IF EXISTS `django_admin_log`;
CREATE TABLE `django_admin_log`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  `object_repr` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `action_flag` smallint UNSIGNED NOT NULL,
  `change_message` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `content_type_id` int NULL DEFAULT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `django_admin_log_content_type_id_c4bce8eb_fk_django_co`(`content_type_id`) USING BTREE,
  INDEX `django_admin_log_user_id_c564eba6_fk_auth_user_id`(`user_id`) USING BTREE,
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of django_admin_log
-- ----------------------------

-- ----------------------------
-- Table structure for django_content_type
-- ----------------------------
DROP TABLE IF EXISTS `django_content_type`;
CREATE TABLE `django_content_type`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `model` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `django_content_type_app_label_model_76bd3d3b_uniq`(`app_label`, `model`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 11 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of django_content_type
-- ----------------------------
INSERT INTO `django_content_type` VALUES (1, 'admin', 'logentry');
INSERT INTO `django_content_type` VALUES (10, 'app01', 'admin');
INSERT INTO `django_content_type` VALUES (8, 'app01', 'department');
INSERT INTO `django_content_type` VALUES (9, 'app01', 'employee');
INSERT INTO `django_content_type` VALUES (7, 'app01', 'order');
INSERT INTO `django_content_type` VALUES (3, 'auth', 'group');
INSERT INTO `django_content_type` VALUES (2, 'auth', 'permission');
INSERT INTO `django_content_type` VALUES (4, 'auth', 'user');
INSERT INTO `django_content_type` VALUES (5, 'contenttypes', 'contenttype');
INSERT INTO `django_content_type` VALUES (6, 'sessions', 'session');

-- ----------------------------
-- Table structure for django_migrations
-- ----------------------------
DROP TABLE IF EXISTS `django_migrations`;
CREATE TABLE `django_migrations`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `app` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 28 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of django_migrations
-- ----------------------------
INSERT INTO `django_migrations` VALUES (1, 'contenttypes', '0001_initial', '2024-11-21 12:50:10.117819');
INSERT INTO `django_migrations` VALUES (2, 'auth', '0001_initial', '2024-11-21 12:50:10.314208');
INSERT INTO `django_migrations` VALUES (3, 'admin', '0001_initial', '2024-11-21 12:50:10.368009');
INSERT INTO `django_migrations` VALUES (4, 'admin', '0002_logentry_remove_auto_add', '2024-11-21 12:50:10.381732');
INSERT INTO `django_migrations` VALUES (5, 'admin', '0003_logentry_add_action_flag_choices', '2024-11-21 12:50:10.386457');
INSERT INTO `django_migrations` VALUES (6, 'app01', '0001_initial', '2024-11-21 12:50:10.470920');
INSERT INTO `django_migrations` VALUES (7, 'contenttypes', '0002_remove_content_type_name', '2024-11-21 12:50:10.526558');
INSERT INTO `django_migrations` VALUES (8, 'auth', '0002_alter_permission_name_max_length', '2024-11-21 12:50:10.550502');
INSERT INTO `django_migrations` VALUES (9, 'auth', '0003_alter_user_email_max_length', '2024-11-21 12:50:10.568299');
INSERT INTO `django_migrations` VALUES (10, 'auth', '0004_alter_user_username_opts', '2024-11-21 12:50:10.573602');
INSERT INTO `django_migrations` VALUES (11, 'auth', '0005_alter_user_last_login_null', '2024-11-21 12:50:10.597788');
INSERT INTO `django_migrations` VALUES (12, 'auth', '0006_require_contenttypes_0002', '2024-11-21 12:50:10.598795');
INSERT INTO `django_migrations` VALUES (13, 'auth', '0007_alter_validators_add_error_messages', '2024-11-21 12:50:10.603700');
INSERT INTO `django_migrations` VALUES (14, 'auth', '0008_alter_user_username_max_length', '2024-11-21 12:50:10.629873');
INSERT INTO `django_migrations` VALUES (15, 'auth', '0009_alter_user_last_name_max_length', '2024-11-21 12:50:10.655880');
INSERT INTO `django_migrations` VALUES (16, 'auth', '0010_alter_group_name_max_length', '2024-11-21 12:50:10.667148');
INSERT INTO `django_migrations` VALUES (17, 'auth', '0011_update_proxy_permissions', '2024-11-21 12:50:10.674290');
INSERT INTO `django_migrations` VALUES (18, 'auth', '0012_alter_user_first_name_max_length', '2024-11-21 12:50:10.701288');
INSERT INTO `django_migrations` VALUES (19, 'sessions', '0001_initial', '2024-11-21 12:50:10.715449');
INSERT INTO `django_migrations` VALUES (20, 'app01', '0002_admin', '2024-11-21 12:55:04.682424');
INSERT INTO `django_migrations` VALUES (21, 'app01', '0003_alter_admin_admin_id_alter_admin_name_and_more', '2024-11-24 05:26:07.636725');
INSERT INTO `django_migrations` VALUES (22, 'app01', '0004_alter_department_created_at_alter_employee_gender', '2024-11-24 06:12:32.879480');
INSERT INTO `django_migrations` VALUES (23, 'app01', '0005_order_order_date', '2024-11-27 04:09:05.821669');
INSERT INTO `django_migrations` VALUES (24, 'app01', '0006_admin_admin_image', '2024-11-28 02:16:33.116423');
INSERT INTO `django_migrations` VALUES (25, 'app01', '0007_alter_admin_admin_image', '2024-11-28 04:20:32.607883');
INSERT INTO `django_migrations` VALUES (26, 'app01', '0008_admin_email_alter_admin_name', '2024-11-29 03:22:11.642733');
INSERT INTO `django_migrations` VALUES (27, 'app01', '0009_alter_admin_admin_image', '2024-11-29 03:38:36.100887');

-- ----------------------------
-- Table structure for django_session
-- ----------------------------
DROP TABLE IF EXISTS `django_session`;
CREATE TABLE `django_session`  (
  `session_key` varchar(40) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `session_data` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`) USING BTREE,
  INDEX `django_session_expire_date_a5c62663`(`expire_date`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of django_session
-- ----------------------------
INSERT INTO `django_session` VALUES ('eaz13ove0tkczr3emfcgltkq4fmapbnc', '.eJw9i8EOgjAQBf_lnRtstTHQk3_SbGQla9xusRwwhH-XePA4mZkNUh6GtEFGpOBQSBkJNKoUOLCSvA4OMYRhOPfxcpvn7m56uF-TRWn6H-1UbaHFumflCbtDbtyaWMm8Vnl_kK4-9t7vX8IVJmw:1tHMcT:ZSu8GkC-8Cx9k3QitSWfUrcn09T1MQLb2utgZ6dNVpk', '2024-12-07 12:30:41.747354');
INSERT INTO `django_session` VALUES ('kwo2zaw6snlgptru4u7y1jkh4yndm0e4', '.eJw9i8EOgjAQBf_lnRtstTHQk3_SbGQla9xusRwwhH-XePA4mZkNUh6GtEFGpOBQSBkJNKoUOLCSvA4OMYRhOPfxcpvn7m56uF-TRWn6H-1UbaHFumflCbtDbtyaWMm8Vnl_kK4-9t7vX8IVJmw:1tINuT:uyBXhRnCdt4LzdhijKJ04iYDh2HRA0CDQrk1zD_seJY', '2024-12-10 08:05:29.769066');
INSERT INTO `django_session` VALUES ('lxf21bazsyowanl169647urshr3m4zaz', '.eJw9i8EOgjAQBf_lnRtstTHQk3_SbGQla9xusRwwhH-XePA4mZkNUh6GtEFGpOBQSBkJNKoUOLCSvA4OMYRhOPfxcpvn7m56uF-TRWn6H-1UbaHFumflCbtDbtyaWMm8Vnl_kK4-9t7vX8IVJmw:1tHjJO:G99TM2H5iqG5vg8SFwxjxWqwyTBePXreLQvnSnPNrkk', '2024-12-08 12:44:30.012415');
INSERT INTO `django_session` VALUES ('quwscqyu3npq64gizdwhz03q2qpspzv3', '.eJw9i8EOgjAQBf_lnRtstTHQk3_SbGQla9xusRwwhH-XePA4mZkNUh6GtEFGpOBQSBkJNKoUOLCSvA4OMYRhOPfxcpvn7m56uF-TRWn6H-1UbaHFumflCbtDbtyaWMm8Vnl_kK4-9t7vX8IVJmw:1tINdn:-Ez4Hq0VnbhnuKbifZNZGZu5BLgVHCPyVUiswUU39lc', '2024-12-10 07:48:15.749178');

SET FOREIGN_KEY_CHECKS = 1;
